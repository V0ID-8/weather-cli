# main.py
# Entry point — temporary test for Step 4.

from weather.favorites import add_favorite, get_favorites, remove_favorite
from weather.api import fetch_current_weather
from weather.cache import save_cache, load_from_cache
from weather.display import print_success, print_info

# --- Test favorites ---
add_favorite("London")
add_favorite("Dubai")
add_favorite("Tokyo")

print_info("Current favorites:")
for city in get_favorites():
    print(f"    {city}")

remove_favorite("Tokyo")

print_info("After removing Tokyo:")
for city in get_favorites():
    print(f"    {city}")

# --- Test cache ---
raw = fetch_current_weather("London")
save_cache("London", "current", raw)

loaded = load_from_cache("London", "current")

if loaded:
    print_success("Cache saved and loaded successfully.")
else:
    print("Cache load failed.")