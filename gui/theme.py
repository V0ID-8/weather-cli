# gui/theme.py
# Central place for all colors, fonts, and sizing used across the GUI.
# Change values here to restyle the entire app at once.


# background
BG_COLOR          = "#0f0f1a"   # Deep dark navy — main window background
BG_GRADIENT_TOP   = "#0f0f1a"   # Top of window
BG_GRADIENT_BOT   = "#1a1a2e"   # Bottom of window

# glass cards
CARD_BG           = "#25252f"   # Frosted glass base
CARD_BORDER       = "#3d3d46"   # Card border
CARD_HOVER        = "#2e2e38"   # Slightly brighter on hover
CARD_RADIUS       = 20          # Corner radius for all cards

# accent colors
ACCENT_BLUE       = "#4fc3f7"   # Primary accent — light sky blue
ACCENT_PURPLE     = "#9b59b6"   # Secondary accent — soft purple
ACCENT_GLOW       = "#2f6989"   # Blue glow effect

# text colors
TEXT_PRIMARY      = "#ffffff"   # Main text — pure white
TEXT_SECONDARY    = "#b0b0b3"   # Subtext
TEXT_MUTED        = "#6f6f76"   # Muted labels
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
