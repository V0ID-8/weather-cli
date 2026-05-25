# Weather CLI

A command-line application that fetches live weather data from OpenWeatherMap
and displays it directly in your terminal — no browser needed.

Built with Python as a learning project focused on clean code structure,
API integration, local caching, and professional Git practices.

---

## Features

- Live current weather for any city in the world
- 5-day forecast displayed as a clean terminal table
- Save and manage favorite cities locally
- Offline mode — falls back to cached data when API is unreachable
- Color-coded terminal output using Colorama
- Clean error messages for invalid cities, bad keys, and no connection

---

## Project Structure

```
weather-cli/
│
│   main.py              # Entry point — CLI argument routing
│   requirements.txt     # Project dependencies
│   .env                 # API key (not committed)
│   .gitignore
│   README.md
│
├── weather/
│       __init__.py      # Marks folder as a Python package
│       api.py           # OpenWeatherMap API calls
│       forecast.py      # Coordinates fetching and cache fallback
│       utils.py         # Parses raw API responses into clean dicts
│       display.py       # All terminal output and formatting
│       favorites.py     # Save/load favorite cities to JSON
│       cache.py         # Local cache for offline fallback
│
├── data/
│       favorites.json   # Saved favorite cities (auto-created)
│
└── cache/
        *.json           # Cached API responses per city (auto-created)
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/V0ID-8/weather-cli.git
cd weather-cli
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root folder:

```
OPENWEATHER_API_KEY=your_api_key_here
```

Get a free API key at: https://openweathermap.org/api

---

## Usage

```bash
# Current weather for a city
python main.py London

# 5-day forecast
python main.py London --forecast

# Save a city to favorites
python main.py save Dubai

# Save a multi-word city
python main.py save "New York"

# List all saved favorites
python main.py favorites

# Remove a city from favorites
python main.py remove Dubai

# Show help
python main.py --help
```

---

## Example Output

```
  London, GB
  ------------------------------------
  Condition   : Partly Cloudy
  Temperature : 18C
  Feels Like  : 17C
  Humidity    : 72%
  Wind        : 14.4 km/h (SW)
  ------------------------------------
```

```
  5-Day Forecast — London

  ╭────────────┬──────┬─────┬────────────────╮
  │ Date       │ High │ Low │ Condition      │
  ╞════════════╪══════╪═════╪════════════════╡
  │ 2024-06-11 │ 19C  │ 14C │ Light Rain     │
  │ 2024-06-12 │ 21C  │ 15C │ Partly Cloudy  │
  │ 2024-06-13 │ 17C  │ 13C │ Overcast Clouds│
  │ 2024-06-14 │ 22C  │ 16C │ Clear Sky      │
  │ 2024-06-15 │ 20C  │ 14C │ Light Rain     │
  ╰────────────┴──────┴─────┴────────────────╯
```

---

## Dependencies

| Library | Version | Purpose |
|---|---|---|
| requests | 2.31.0 | HTTP requests to the weather API |
| python-dotenv | 1.0.0 | Load API key from .env file |
| colorama | 0.4.6 | Terminal color output on Windows |
| tabulate | 0.9.0 | Forecast table formatting |

---

## Author

**Talal Al-Bulushi**
GitHub: https://github.com/V0ID-8