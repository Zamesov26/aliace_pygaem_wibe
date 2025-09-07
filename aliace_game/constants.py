"""
Constants for the Elias game.
This module contains all the constants used throughout the game.
"""

# Screen dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Font sizes
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 24

# Game settings
DEFAULT_GAME_DURATION = 120  # 2 minutes default

# Time options (in seconds)
TIME_OPTIONS = [
    60,   # 1 minute
    120,  # 2 minutes
    180,  # 3 minutes
    240,  # 4 minutes
    300   # 5 minutes
]

# Screen identifiers
SCREEN_MENU = "menu"
SCREEN_GAME = "game"
SCREEN_RESULTS = "results"
SCREEN_MANAGE = "manage"