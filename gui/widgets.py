# gui/widgets.py
# All reusable UI components used by app.py.
# Each widget is a self-contained class that handles its own layout.

import customtkinter as ctk
from gui.theme import *


class GlassFrame(ctk.CTkFrame):
    """
    Base glass card component.
    All weather cards inherit from this for consistent styling.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=CARD_RADIUS,
            **kwargs,
        )


# search bar

class SearchBar(ctk.CTkFrame):
    """
    Top search bar with a text input and search button.
    Calls on_search(city) when the user submits.
    """

    def __init__(self, parent, on_search, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.on_search = on_search
        self.grid_columnconfigure(0, weight=1)

        # Glass container
        container = GlassFrame(self)
        container.grid(row=0, column=0, sticky="ew")
        container.grid_columnconfigure(0, weight=1)

        # Text input
        self.entry = ctk.CTkEntry(
            container,
            placeholder_text="Search city...",
            font=FONT_SEARCH,
            fg_color="transparent",
            border_width=0,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_MUTED,
            height=48,
        )
        self.entry.grid(row=0, column=0, padx=PADDING_MD, sticky="ew")

        # Search button
        ctk.CTkButton(
            container,
            text="Search",
            font=FONT_BUTTON,
            fg_color=ACCENT_BLUE,
            text_color="#000000",
            hover_color=ACCENT_PURPLE,
            corner_radius=12,
            width=100,
            height=36,
            command=self._submit,
        ).grid(row=0, column=1, padx=(0, PADDING_SM), pady=PADDING_SM)

        # Bind Enter key to search
        self.entry.bind("<Return>", lambda e: self._submit())


    def _submit(self):
        """Read the entry value and call the search callback."""
        city = self.entry.get().strip()
        if city:
            self.on_search(city)


# current weather card

class WeatherCard(GlassFrame):
    """
    Large card showing current weather conditions.
    Displays temp, feels like, humidity, wind, and description.
    """

    def __init__(self, parent, weather: dict, on_save, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        p = PADDING_LG

        # --- Left side: main weather info ---
        left = ctk.CTkFrame(self, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=p, pady=p)

        # City name
        ctk.CTkLabel(
            left,
            text=f"{weather['city']}, {weather['country']}",
            font=FONT_TITLE,
            text_color=TEXT_PRIMARY,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        # Weather description
        ctk.CTkLabel(
            left,
            text=weather["description"],
            font=FONT_SUBTITLE,
            text_color=TEXT_SECONDARY,
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(2, PADDING_MD))

        # Big temperature display
        ctk.CTkLabel(
            left,
            text=f"{weather['temp']}°C",
            font=FONT_HUGE,
            text_color=ACCENT_BLUE,
            anchor="w",
        ).grid(row=2, column=0, sticky="w")

        # Feels like
        ctk.CTkLabel(
            left,
            text=f"Feels like  {weather['feels_like']}°C",
            font=FONT_SMALL,
            text_color=TEXT_MUTED,
            anchor="w",
        ).grid(row=3, column=0, sticky="w", pady=(4, 0))

        # --- Right side: detail stats ---
        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=1, sticky="ne", padx=p, pady=p)

        # Save button
        ctk.CTkButton(
            right,
            text="+ Save",
            font=FONT_BUTTON,
            fg_color="transparent",
            border_color=ACCENT_BLUE,
            border_width=1,
            text_color=ACCENT_BLUE,
            hover_color=CARD_HOVER,
            corner_radius=12,
            width=90,
            height=32,
            command=on_save,
        ).grid(row=0, column=0, sticky="e", pady=(0, PADDING_LG))

        # Stat rows
        stats = [
            ("Humidity",   f"{weather['humidity']}%"),
            ("Wind",       f"{weather['wind_speed']} km/h"),
            ("Direction",  _wind_direction(weather["wind_deg"])),
        ]

        for i, (label, value) in enumerate(stats):
            _stat_row(right, label, value, row=i + 1)

# forecast day card

class ForecastCard(GlassFrame):
    """
    Small card for a single forecast day.
    Shows date, condition, high and low temperature.
    """

    def __init__(self, parent, day: dict, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        p = PADDING_MD

        # Date label — show only month and day
        date_short = day["date"][5:]  # e.g. "06-11" from "2024-06-11"
        ctk.CTkLabel(
            self,
            text=date_short,
            font=FONT_SMALL,
            text_color=TEXT_MUTED,
        ).grid(row=0, column=0, pady=(p, PADDING_XS))

        # Condition
        ctk.CTkLabel(
            self,
            text=day["description"],
            font=FONT_TINY,
            text_color=TEXT_SECONDARY,
            wraplength=120,
            justify="center",
        ).grid(row=1, column=0, padx=PADDING_SM)

        # High temperature
        ctk.CTkLabel(
            self,
            text=f"{round(day['temp_max'])}°",
            font=FONT_TITLE,
            text_color=ACCENT_BLUE,
        ).grid(row=2, column=0, pady=(PADDING_SM, 0))

        # Low temperature
        ctk.CTkLabel(
            self,
            text=f"{round(day['temp_min'])}°",
            font=FONT_SMALL,
            text_color=TEXT_MUTED,
        ).grid(row=3, column=0, pady=(0, p))


# favorite city item

class FavoriteItem(ctk.CTkFrame):
    """
    A single row in the favorites sidebar.
    Clicking the city name loads its weather.
    The x button removes it from favorites.
    """

    def __init__(self, parent, city: str, on_click, on_remove, **kwargs):
        super().__init__(
            parent,
            fg_color=CARD_BG,
            corner_radius=10,
            **kwargs,
        )

        self.grid_columnconfigure(0, weight=1)

        # City name button — loads weather on click
        ctk.CTkButton(
            self,
            text=city,
            font=FONT_SMALL,
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=CARD_HOVER,
            anchor="w",
            command=lambda: on_click(city),
        ).grid(row=0, column=0, sticky="ew", padx=(PADDING_XS, 0))

        # Remove button
        ctk.CTkButton(
            self,
            text="x",
            font=FONT_TINY,
            fg_color="transparent",
            text_color=TEXT_MUTED,
            hover_color="#3a1515",
            width=28,
            command=lambda: on_remove(city),
        ).grid(row=0, column=1, padx=(0, PADDING_XS))


# status banner

class StatusBanner(ctk.CTkFrame):
    """
    A thin banner shown above content for success or warning messages.
    Warning=True shows yellow. Warning=False shows green.
    """

    def __init__(self, parent, message: str, warning: bool = False, **kwargs):
        color = "#2e2117" if warning else "#0d2e28"
        text_color = "#ffcc00" if warning else "#00ff88"

        super().__init__(
            parent,
            fg_color=color,
            corner_radius=10,
            **kwargs,
        )

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text=message,
            font=FONT_SMALL,
            text_color=text_color,
            anchor="w",
        ).grid(row=0, column=0, padx=PADDING_MD, pady=PADDING_XS, sticky="w")


# private helpers

def _stat_row(parent, label: str, value: str, row: int):
    """Render a label-value pair in two columns."""

    ctk.CTkLabel(
        parent,
        text=label,
        font=FONT_TINY,
        text_color=TEXT_MUTED,
        anchor="e",
    ).grid(row=row, column=0, sticky="e", padx=(0, PADDING_XS), pady=2)

    ctk.CTkLabel(
        parent,
        text=value,
        font=FONT_SMALL,
        text_color=TEXT_PRIMARY,
        anchor="w",
    ).grid(row=row, column=1, sticky="w", pady=2)


def _wind_direction(degrees: int) -> str:
    """Convert wind degrees to a compass label."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return directions[round(degrees / 45) % 8]
