#!/usr/bin/env python3
"""
This module is used to interact with a Redis instance to perform basic
reads and writes for caching and storing data
"""
import redis
import uuid
from typing import Union


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
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
