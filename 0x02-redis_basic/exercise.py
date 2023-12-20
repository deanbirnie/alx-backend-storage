#!/usr/bin/env python3
"""
This module is used to interact with a Redis instance to perform basic
reads and writes for caching and storing data
"""
import redis
import uuid
from typing import Union, Callable


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
