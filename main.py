# main.py
# Entry point — temporary test for Step 2.

from weather.api import fetch_current_weather

data = fetch_current_weather("London")
print(data)