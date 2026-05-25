# weather/forecast.py
# Coordinates fetching, caching, and returning weather data.
# This is the middle layer between main.py and the API/cache modules.

from weather.api import fetch_current_weather, fetch_forecast
from weather.cache import (
    save_cache,
    load_from_cache,
    load_from_cache_any_age,
)


def get_current_weather(city: str) -> tuple[dict, bool]:
    """
    Try to fetch live current weather for a city.
    On success, save the result to cache and return it.
    On failure, fall back to cached data (any age).

    Returns:
        (data dict, is_cached bool)
        is_cached is True if the data came from cache, not a live fetch.
    """
    try:
        data = fetch_current_weather(city)
        save_cache(city, "current", data)
        return data, False

    except Exception:
        # Live fetch failed — try cache
        cached = load_from_cache_any_age(city, "current")
        if cached:
            return cached, True
        # Nothing available at all — re-raise the original error
        raise


def get_forecast(city: str) -> tuple[dict, bool]:
    """
    Try to fetch a live 5-day forecast for a city.
    On success, save the result to cache and return it.
    On failure, fall back to cached data (any age).

    Returns:
        (data dict, is_cached bool)
        is_cached is True if the data came from cache, not a live fetch.
    """
    try:
        data = fetch_forecast(city)
        save_cache(city, "forecast", data)
        return data, False

    except Exception:
        cached = load_from_cache_any_age(city, "forecast")
        if cached:
            return cached, True
        raise