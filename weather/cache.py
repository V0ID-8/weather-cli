# weather/cache.py
# Saves and loads the last successful API response for each city.
# Used as a fallback when the user is offline or the API is unreachable.

import json
import os
import time


#folder to store cached data
CACHE_DIR = "cache"


#how long cached data is considered valid (in seconds)
CACHE_MAX_AGE = 60 * 60 * 3  #3 hours


def get_cache_path(city: str, data_type: str) -> str:
    """
    Build the file path for a cache entry.
    Example: cache/london_current.json
    """
    safe_name = city.strip().lower().replace(" ", "_")
    return os.path.join(CACHE_DIR, f"{safe_name}_{data_type}.json")


def save_cache(city: str, data_type: str, data: dict) -> None:
    """Save API response data to a cache file."""
    os.makedirs(CACHE_DIR, exist_ok=True)  # Ensure cache directory exists

    payload = {
        "timestamp": time.time(),
        "data": data
    }

    with open(get_cache_path(city, data_type), "w") as f:
        json.dump(payload, f, indent=2)


def load_from_cache(city: str, data_type: str) -> dict:
    """
    Load cached data for a city and type (current or forecast).
    Returns the data if it's still valid, or None if it's too old or missing.
    """
    path = get_cache_path(city, data_type)

    if not os.path.exists(path):
        return None  # No cache file

    with open(path, "r") as f:
        payload = json.load(f)

    age = time.time() - payload["timestamp"]
    if age > CACHE_MAX_AGE:
        return None  # Cache is too old

    return payload["data"]


def cache_exists(city: str, data_type: str) -> bool:
    """
    Check if any cache file exists for a city, regardless of age.
    Used as a last resort fallback when even expired cache is better than nothing.
    """
    return os.path.exists(get_cache_path(city, data_type))


def load_from_cache_any_age(city: str, data_type: str) -> dict | None:
    """
    Load a cache entry even if it is expired.
    Only used when the API is unreachable and fresh cache is unavailable.
    """
    path = get_cache_path(city, data_type)

    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        payload = json.load(f)

    return payload["data"]