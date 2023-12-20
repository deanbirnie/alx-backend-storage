#!/usr/bin/env python3
"""
This module can be used as an expiring web cache and tracker
"""
import requests
import redis


def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL and cache the result.
    """
    redis_client = redis.Redis()

    count_key = f"count:{url}"

    redis_client.incr(count_key)
    redis_client.expire(count_key, 10)

    response = requests.get(url)
    html_content = response.text

    return html_content
