# main.py
# Entry point for the Weather CLI app.
# Parses command-line arguments and routes to the correct action.

import sys
from weather.forecast import get_current_weather, get_forecast
from weather.utils import parse_current_weather, parse_forecast
from weather.display import (
    print_current_weather,
    print_forecast,
    print_error,
    print_success,
    print_info,
)
from weather.favorites import add_favorite, remove_favorite, get_favorites


def show_help() -> None:
    """Print usage instructions to the terminal."""
    print()
    print("  Usage:")
    print("    python main.py <city>                 Show current weather")
    print("    python main.py <city> --forecast      Show 5-day forecast")
    print("    python main.py save <city>            Save city to favorites")
    print("    python main.py remove <city>          Remove city from favorites")
    print("    python main.py favorites              List all saved cities")
    print("    python main.py --help                 Show this help message")
    print()


def handle_weather(city: str, show_forecast: bool) -> None:
    """
    Fetch and display current weather or forecast for a city.
    Falls back to cache automatically if the API is unreachable.
    """
    try:
        if show_forecast:
            raw, cached = get_forecast(city)
            forecast = parse_forecast(raw)
            print_forecast(forecast, city.title(), cached=cached)
        else:
            raw, cached = get_current_weather(city)
            weather = parse_current_weather(raw)
            print_current_weather(weather, cached=cached)

    except ValueError as e:
        # City not found
        print_error(str(e))

    except PermissionError as e:
        # Bad API key
        print_error(str(e))

    except (ConnectionError, TimeoutError, Exception) as e:
        # Network issue and no cache available
        print_error(f"Could not retrieve weather data. {str(e)}")


def handle_save(city: str) -> None:
    """Save a city to favorites and confirm to the user."""
    if not city:
        print_error("Please provide a city name. Example: python main.py save Dubai")
        return

    added = add_favorite(city)
    if added:
        print_success(f"{city.title()} added to favorites.")
    else:
        print_info(f"{city.title()} is already in your favorites.")


def handle_remove(city: str) -> None:
    """Remove a city from favorites and confirm to the user."""
    if not city:
        print_error("Please provide a city name. Example: python main.py remove Dubai")
        return

    removed = remove_favorite(city)
    if removed:
        print_success(f"{city.title()} removed from favorites.")
    else:
        print_info(f"{city.title()} was not found in your favorites.")


def handle_favorites() -> None:
    """Display all saved favorite cities."""
    cities = get_favorites()

    if not cities:
        print_info("No favorites saved yet. Use: python main.py save <city>")
        return

    print()
    print("  Saved Cities:")
    for city in cities:
        print(f"    - {city}")
    print()


def main() -> None:
    """
    Parse arguments and route to the correct handler.
    Expects at least one argument after the script name.
    """
    args = sys.argv[1:]  # Everything after "python main.py"

    # No arguments given
    if not args:
        show_help()
        return

    first = args[0].lower()

    # Help flag
    if first == "--help":
        show_help()
        return

    # Favorites list
    if first == "favorites":
        handle_favorites()
        return

    # Save a city
    if first == "save":
        city = " ".join(args[1:])
        handle_save(city)
        return

    # Remove a city
    if first == "remove":
        city = " ".join(args[1:])
        handle_remove(city)
        return

    # Weather or forecast for a city
    # City name is everything before --forecast flag
    if "--forecast" in args:
        args.remove("--forecast")
        city = " ".join(args)
        handle_weather(city, show_forecast=True)
    else:
        city = " ".join(args)
        handle_weather(city, show_forecast=False)


if __name__ == "__main__":
    main()