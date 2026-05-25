# weather/api.py
# Handles all communication with the OpenWeatherMap API.

import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#Base URL for OpenWeatherMap API
BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_api_key():
    """Retrieves the OpenWeatherMap API key from environment variables."""
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        raise EnvironmentError("API key not found. Make sure OPENWEATHER_API_KEY is set in your .env file.")
    return key


def fetch_current_weather(city: str) -> dict:
    """Fetches current weather data for a given city."""
    api_key = get_api_key()

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",  #Celsius
        "lang": "en"  #English
    }

    try:
        response = requests.get(f"{BASE_URL}/weather", params=params, timeout=10)

        # 404 means the city name was not recognized
        if response.status_code == 404:
            raise ValueError(f"City '{city}' not found. Check the spelling and try again.")

        # 401 means the API key is invalid or not yet activated
        if response.status_code == 401:
            raise PermissionError("Invalid API key. Check your .env file.")

        # Raise an error for any other bad status codes
        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        raise ConnectionError("No internet connection. Try again when you are online.")

    except requests.exceptions.Timeout:
        raise TimeoutError("The request timed out. The API may be slow — try again.")
    

def fetch_forecast(city: str) -> dict:
    """Fetches 5-day weather forecast data for a given city."""
    
    api_key = get_api_key()

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "en"
    }
    try:
        response = requests.get(f"{BASE_URL}/forecast", params=params, timeout=10)

        if response.status_code == 404:
            raise ValueError(f"City '{city}' not found. Check the spelling and try again.")

        if response.status_code == 401:
            raise PermissionError("Invalid API key. Check your .env file.")

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        raise ConnectionError("No internet connection. Try again when you are online.")

    except requests.exceptions.Timeout:
        raise TimeoutError("The request timed out. The API may be slow — try again.")  