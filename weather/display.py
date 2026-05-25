#weather/display.py
#all terminal output lives here. nothing is printed from other modules.

from colorama import init, Fore, Style
from tabulate import tabulate
from weather.utils import wind_direction

#initialize colorama for windows terminal color support
init(autoreset=True)


def print_current_weather(weather: dict, cached: bool = False) -> None:
    """
    Print a clean, formatted current weather block to the terminal.
    If cached is True, show a warning that the data is not live.
    """
    print()

    # Show a warning banner if this data came from cache
    if cached:
        print(Fore.YELLOW + "  [OFFLINE] Showing cached data — live fetch failed.")
        print()

    # City header
    print(Fore.CYAN + Style.BRIGHT + f"  {weather['city']}, {weather['country']}")
    print(Fore.WHITE + "  " + "-" * 36)

    # Core weather details
    print(Fore.WHITE + f"  Condition   : " + Fore.GREEN  + f"{weather['description']}")
    print(Fore.WHITE + f"  Temperature : " + Fore.YELLOW + f"{weather['temp']}C")
    print(Fore.WHITE + f"  Feels Like  : " + Fore.YELLOW + f"{weather['feels_like']}C")
    print(Fore.WHITE + f"  Humidity    : " + Fore.CYAN   + f"{weather['humidity']}%")
    print(
        Fore.WHITE + f"  Wind        : " +
        Fore.CYAN  + f"{weather['wind_speed']} km/h " +
        Fore.WHITE + f"({wind_direction(weather['wind_deg'])})"
    )

    print(Fore.WHITE + "  " + "-" * 36)
    print()


def print_forecast(forecast: list, city: str, cached: bool = False) -> None:
    """
    Print a clean 5-day forecast table to the terminal.
    If cached is True, show a warning that the data is not live.
    """
    print()

    if cached:
        print(Fore.YELLOW + "  [OFFLINE] Showing cached data — live fetch failed.")
        print()

    print(Fore.CYAN + Style.BRIGHT + f"  5-Day Forecast - {city}")
    print()

    # Build rows for the table
    rows = []
    for day in forecast:
        rows.append([
            day["date"],
            f"{round(day['temp_max'])}C",
            f"{round(day['temp_min'])}C",
            day["description"],
        ])

    headers = ["Date", "High", "Low", "Condition"]

    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print()


def print_error(message: str) -> None:
    """Print a formatted error message in red."""
    print()
    print(Fore.RED + f"  Error: {message}")
    print()


def print_success(message: str) -> None:
    """Print a formatted success message in green."""
    print()
    print(Fore.GREEN + f"  {message}")
    print()


def print_info(message: str) -> None:
    """Print a neutral info message in cyan."""
    print()
    print(Fore.CYAN + f"  {message}")
    print()