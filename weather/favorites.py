# weather/favorites.py
# handles saving and loading favorite cities to a local JSON file.

import json
import os

#path to the favorites file where favorite are stored
FAVORITES_FILE = os.path.join("data", "favorites.json")


def load_favorites() -> list:
    """Load the list of favorite cities from the JSON file."""
    if not os.path.exists(FAVORITES_FILE):
        return []  # No favorites yet

    with open(FAVORITES_FILE, "r") as f:
        return json.load(f)
    

def save_favorites(favorites: list) -> None:
    """Save the list of favorite cities to the JSON file."""
    os.makedirs("data", exist_ok=True)  # Ensure the data directory exists

    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=4)


def add_favorite(city: str) -> bool:
    """Add a city to the favorites list. Returns True if added, False if already in favorites."""
    favorites = load_favorites()

    if city in favorites:
        return False  # Already a favorite
    
    favorites.append(city)
    save_favorites(favorites)
    return True


def remove_favorite(city: str) -> bool:
    """Remove a city from the favorites list. Returns True if removed, False if not found."""
    favorites = load_favorites()

    if city not in favorites:
        return False  
    
    favorites.remove(city)
    save_favorites(favorites)
    return True


def get_favorites() -> list:
    """Get the current list of favorite cities."""
    return load_favorites()