# weather/utils.py
# Helper functions for parsing raw API data into clean usable values.


def parse_current_weather(data: dict) -> dict:
    """
    Extract and clean the fields we need from raw current weather API response.
    Returns a flat dictionary with only what the display needs.
    """
    return {
        "city"        : data["name"],
        "country"     : data["sys"]["country"],
        "temp"        : round(data["main"]["temp"]),
        "feels_like"  : round(data["main"]["feels_like"]),
        "humidity"    : data["main"]["humidity"],
        "description" : data["weather"][0]["description"].title(),
        "wind_speed"  : round(data["wind"]["speed"] * 3.6, 1),  # Convert m/s to km/h
        "wind_deg"    : data["wind"].get("deg", 0),
    }


def parse_forecast(data: dict) -> list:
    """
    Extract daily high/low temps and conditions from the 5-day forecast response.
    The API returns data in 3-hour intervals — we group them by date.
    Returns a list of dicts, one per unique day.
    """
    daily = {}

    for entry in data["list"]:
        # The date portion of the timestamp e.g. "2024-06-10"
        date = entry["dt_txt"].split(" ")[0]

        temp = entry["main"]["temp"]
        description = entry["weather"][0]["description"].title()

        if date not in daily:
            daily[date] = {
                "date"        : date,
                "temp_min"    : temp,
                "temp_max"    : temp,
                "description" : description,
            }
        else:
            # Keep track of the lowest and highest temps seen for that day
            daily[date]["temp_min"] = min(daily[date]["temp_min"], temp)
            daily[date]["temp_max"] = max(daily[date]["temp_max"], temp)

    # Return as a list, skip the first entry (it may be a partial day)
    days = list(daily.values())
    return days[1:6]  # Return up to 5 full days


def wind_direction(deg: int) -> str:
    """Convert wind direction in degrees to a compass direction."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = round(deg / 45) % 8
    return directions[idx]


    
