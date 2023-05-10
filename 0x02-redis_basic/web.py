#!/usr/bin/env python3

"""
This module implements a web page caching and tracking functionality using Redis.
"""

import redis
import requests
from functools import wraps
from typing import Callable


# Connect to Redis
redis_client = redis.Redis()


def cache_with_expiration(expiration: int) -> Callable:
    """
    Decorator to cache the result of a function with an expiration time.

    Args:
        expiration: The expiration time in seconds.

    Returns:
        The decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Check if the URL exists in the cache
            cached_result = redis_client.get(url)
            if cached_result:
                return cached_result.decode('utf-8')

            # If not in cache, retrieve the page content
            page_content = func(url)

            # Cache the page content with expiration time
            redis_client.setex(url, expiration, page_content)

            return page_content

        return wrapper

    return decorator


def track_requests(func: Callable) -> Callable:
    """
    Decorator to track the number of times a URL is accessed.

    Args:
        func: The function to be decorated.

    Returns:
        The decorator function.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the request count for the URL
        redis_client.incr(f"count:{url}")

        return func(url)

    return wrapper


@cache_with_expiration(10)
@track_requests
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL.

    Args:
        url: The URL to retrieve the content from.

    Returns:
        The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    # Example usage
    url = 'http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com'
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))

    # Check the request count for the URL
    request_count = redis_client.get(f"count:{url}")
    if request_count:
        print(f"Request count for {url}: {int(request_count)}")

