# gui/app.py
# Main application window and layout controller.
# Handles the root window, sidebar, search bar, and content area.

import customtkinter as ctk
from gui.theme import *
from gui.widgets import (
    WeatherCard,
    ForecastCard,
    FavoriteItem,
    SearchBar,
    StatusBanner,
)

from weather.forecast import get_current_weather, get_forecast
from weather.utils import parse_current_weather, parse_forecast
from weather.favorites import add_favorite, remove_favorite, get_favorites


# tell customtkinter to use dark mode always
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WeatherApp(ctk.CTk):
    """Main application class for the Weather GUI."""
    
    def __init__(self):
        super().__init__()

        # --- Window setup ---
        self.title("Weather")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_W, WINDOW_MIN_H)
        self.configure(fg_color=BG_COLOR)

        # Track current state
        self.current_city  = None
        self.status_banner = None

        # Build the full layout
        self._build_layout()

        # Load a default city on startup
        self._search_city("London")

# layout builders

    def _build_layout(self):
        """Create the three main layout regions: sidebar, header, content."""

        # Root uses two columns: sidebar | main
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()


    def _build_sidebar(self):
        """Left sidebar containing the app title and favorites list."""

        self.sidebar = ctk.CTkFrame(
            self,
            width=SIDEBAR_WIDTH,
            fg_color="#12122088",
            corner_radius=0,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(2, weight=1)

        # App title
        ctk.CTkLabel(
            self.sidebar,
            text="Weather",
            font=FONT_TITLE,
            text_color=ACCENT_BLUE,
        ).grid(row=0, column=0, padx=PADDING_LG, pady=(PADDING_LG, PADDING_XS), sticky="w")

        ctk.CTkLabel(
            self.sidebar,
            text="Favorites",
            font=FONT_SMALL,
            text_color=TEXT_MUTED,
        ).grid(row=1, column=0, padx=PADDING_LG, pady=(0, PADDING_SM), sticky="w")

        # Scrollable area for favorite cities
        self.favorites_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent",
            scrollbar_button_color=CARD_BORDER,
        )
        self.favorites_frame.grid(row=2, column=0, sticky="nsew", padx=PADDING_SM, pady=PADDING_SM)
        self.favorites_frame.grid_columnconfigure(0, weight=1)

        # Refresh button at bottom of sidebar
        ctk.CTkButton(
            self.sidebar,
            text="Refresh",
            font=FONT_BUTTON,
            fg_color=ACCENT_BLUE,
            text_color="#000000",
            corner_radius=12,
            height=36,
            command=self._refresh,
        ).grid(row=3, column=0, padx=PADDING_LG, pady=PADDING_MD, sticky="ew")

        self._refresh_favorites_list()

    def _build_main(self):
        """Right side containing search bar and all weather content."""

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=PADDING_LG, pady=PADDING_LG)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Search bar at top
        self.search_bar = SearchBar(self.main_frame, on_search=self._search_city)
        self.search_bar.grid(row=0, column=0, sticky="ew", pady=(0, PADDING_MD))

        # Scrollable content area below search
        self.content = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            scrollbar_button_color=CARD_BORDER,
        )
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)


    # data loading and display

    def _search_city(self, city: str):
        """Fetch weather for a city and update the display."""

        city = city.strip()
        if not city:
            return

        self.current_city = city
        self._clear_content()

        # --- Current weather ---
        try:
            raw, cached = get_current_weather(city)
            weather = parse_current_weather(raw)

            if cached:
                self._show_banner("Offline — showing cached data.", warning=True)

            WeatherCard(
                self.content,
                weather=weather,
                on_save=self._save_current_city,
            ).grid(row=0, column=0, sticky="ew", pady=(0, PADDING_MD))

        except ValueError:
            self._show_banner(f"City '{city}' not found. Check the spelling.", warning=True)
            return
        except Exception as e:
            self._show_banner(f"Could not load weather. {str(e)}", warning=True)
            return

        # --- Forecast ---
        try:
            raw_fc, cached_fc = get_forecast(city)
            forecast = parse_forecast(raw_fc)
            self._build_forecast_row(forecast)

        except Exception:
            pass  # Forecast failure is non-critical — current weather still shows


    def _build_forecast_row(self, forecast: list):
        """Build a responsive row of forecast day cards."""

        label = ctk.CTkLabel(
            self.content,
            text="5-Day Forecast",
            font=FONT_TITLE,
            text_color=TEXT_SECONDARY,
        )
        label.grid(row=1, column=0, sticky="w", pady=(PADDING_SM, PADDING_XS))

        row_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        row_frame.grid(row=2, column=0, sticky="ew")

        for i, day in enumerate(forecast):
            row_frame.grid_columnconfigure(i, weight=1)
            ForecastCard(row_frame, day=day).grid(
                row=0, column=i,
                padx=PADDING_XS,
                sticky="nsew",
            )


    # favorites management

    def _save_current_city(self):
        """Save the currently displayed city to favorites."""

        if not self.current_city:
            return

        added = add_favorite(self.current_city)
        if added:
            self._show_banner(f"{self.current_city.title()} saved to favorites.", warning=False)
            self._refresh_favorites_list()
        else:
            self._show_banner(f"{self.current_city.title()} is already in favorites.", warning=True)


    def _refresh_favorites_list(self):
        """Rebuild the favorites list in the sidebar."""

        for widget in self.favorites_frame.winfo_children():
            widget.destroy()

        cities = get_favorites()

        if not cities:
            ctk.CTkLabel(
                self.favorites_frame,
                text="No favorites yet.\nSearch a city and\nclick Save.",
                font=FONT_TINY,
                text_color=TEXT_MUTED,
                justify="left",
            ).grid(row=0, column=0, padx=PADDING_SM, pady=PADDING_SM, sticky="w")
            return

        for i, city in enumerate(cities):
            FavoriteItem(
                self.favorites_frame,
                city=city,
                on_click=self._search_city,
                on_remove=self._remove_favorite,
            ).grid(row=i, column=0, sticky="ew", pady=2)


    def _remove_favorite(self, city: str):
        """Remove a city from favorites and refresh the sidebar."""

        remove_favorite(city)
        self._refresh_favorites_list()

        if self.current_city and self.current_city.lower() == city.lower():
            self._show_banner(f"{city} removed from favorites.", warning=False)


    # helpers

    def _refresh(self):
        """Re-fetch weather for the current city."""

        if self.current_city:
            self._search_city(self.current_city)


    def _clear_content(self):
        """Remove all widgets from the content area."""

        for widget in self.content.winfo_children():
            widget.destroy()

        if self.status_banner:
            self.status_banner.destroy()
            self.status_banner = None


    def _show_banner(self, message: str, warning: bool = False):
        """Show a status banner above the content area."""

        if self.status_banner:
            self.status_banner.destroy()

        self.status_banner = StatusBanner(
            self.main_frame,
            message=message,
            warning=warning,
        )
        self.status_banner.grid(row=0, column=0, sticky="ew", pady=(0, PADDING_SM))            