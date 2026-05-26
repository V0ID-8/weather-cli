# main_gui.py
# Entry point for the GUI version of the Weather app.
# Run this file to launch the desktop window.

from gui.app import WeatherApp

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()

    