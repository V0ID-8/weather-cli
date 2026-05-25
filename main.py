# main.py
# Entry point — temporary test for Step 3.

from weather.api import fetch_current_weather, fetch_forecast
from weather.utils import parse_current_weather, parse_forecast
from weather.display import print_current_weather, print_forecast

# Test city
city = "London"

# Fetch and display current weather
raw_current = fetch_current_weather(city)
weather = parse_current_weather(raw_current)
print_current_weather(weather)

# Fetch and display forecast
raw_forecast = fetch_forecast(city)
forecast = parse_forecast(raw_forecast)
print_forecast(forecast, city)