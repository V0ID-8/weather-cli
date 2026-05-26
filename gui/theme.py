# gui/theme.py
# Central place for all colors, fonts, and sizing used across the GUI.
# Change values here to restyle the entire app at once.


# background
BG_COLOR          = "#0f0f1a"   # Deep dark navy — main window background
BG_GRADIENT_TOP   = "#0f0f1a"   # Top of window
BG_GRADIENT_BOT   = "#1a1a2e"   # Bottom of window

# glass cards
CARD_BG           = "#ffffff18" # White at 9% opacity — frosted glass base
CARD_BORDER       = "#ffffff30" # White at 19% opacity — card border
CARD_HOVER        = "#ffffff22" # Slightly brighter on hover
CARD_RADIUS       = 20          # Corner radius for all cards

# accent colors
ACCENT_BLUE       = "#4fc3f7"   # Primary accent — light sky blue
ACCENT_PURPLE     = "#9b59b6"   # Secondary accent — soft purple
ACCENT_GLOW       = "#4fc3f780" # Blue at 50% opacity — glow effect

# text colors
TEXT_PRIMARY      = "#ffffff"   # Main text — pure white
TEXT_SECONDARY    = "#ffffffaa" # Subtext — white at 67% opacity
TEXT_MUTED        = "#ffffff66" # Muted labels — white at 40% opacity
TEXT_ACCENT       = "#4fc3f7"   # Highlighted values

# fonts
FONT_FAMILY       = "Segoe UI"  # good font available on Windows

FONT_HUGE         = (FONT_FAMILY, 52, "bold")    # Temperature display
FONT_TITLE        = (FONT_FAMILY, 22, "bold")    # City name
FONT_SUBTITLE     = (FONT_FAMILY, 14)            # Country, description
FONT_LABEL        = (FONT_FAMILY, 12)            # Field labels
FONT_SMALL        = (FONT_FAMILY, 11)            # Secondary info
FONT_TINY         = (FONT_FAMILY, 10)            # Muted details
FONT_BUTTON       = (FONT_FAMILY, 13, "bold")    # Buttons
FONT_SEARCH       = (FONT_FAMILY, 14)            # Search bar input

# sizing
WINDOW_WIDTH      = 1100        # Default window width
WINDOW_HEIGHT     = 720         # Default window height
WINDOW_MIN_W      = 900         # Minimum window width
WINDOW_MIN_H      = 600         # Minimum window height

PADDING_LG        = 24          # Large padding
PADDING_MD        = 16          # Medium padding
PADDING_SM        = 10          # Small padding
PADDING_XS        = 6           # Extra small padding

SIDEBAR_WIDTH     = 220         # Favorites sidebar width\
