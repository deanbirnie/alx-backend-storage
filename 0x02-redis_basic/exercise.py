#!/usr/bin/env python3
"""
This module is used to interact with a Redis instance to perform basic
reads and writes for caching and storing data
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
        """
        Decorator to store the history of inputs and outputs for a function.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = f"{method.__qualname__}:inputs"
            output_key = f"{method.__qualname__}:outputs"

            self._redis.rpush(input_key, str(args))
            output = method(self, *args, **kwargs)

            self._redis.rpush(output_key, output)
            return output
        return wrapper

def replay(method: Callable):
        """
        Display the history of calls of a particular function
        """
        method_name = method.__qualname__
        inputs = cache._redis.lrange(f"{method_name}:inputs", 0, -1)
        outputs = cache._redis.lrange(f"{method_name}:outputs", 0, -1)

        print(f"{method_name} was called {len(inputs)} times:")
        for input_args, output in zip(inputs, outputs):
            input_str = input_args.decode()
            output_str = output.decode()
            print(f"{method_name}(*{input_str}) -> {output_str}")


class Cache:
    """
    This class defines the methods and attributes we'll use for our
    Redis caching instance
    """
    def __init__(self):
        """
        Instantiation of the cache object
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Takes in data and returns a randomly generated key
        which is used to store the data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, None]:
        """
        This method is used to convert the data back to the desired
        format from the string format Redis stores it as.
        """
        result = self._redis.get(key)
        if result is None:
            return None
        if fn:
            return fn(result)
        return result

    def get_str(self, key: str) -> Union[str, None]:
        """
        Parametrize Cache.get with the correct conversion function for
        strings.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8") if isinstance(
            d, bytes
        ) else d)

    def get_int(self, key: str) -> Union[int, None]:
        """
        Parametrize Cache.get with the correct conversion function for
        integers.
        """
        return self.get(key, fn=int)
