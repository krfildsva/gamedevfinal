# settings.py

# Basic game parameters
DEFAULT_ROWS = 3
DEFAULT_COLS = 3

CARD_SIZE = 100
GAP = 10
MARGIN = 120   # Increased margin so the board appears lower (adjust as desired)

# Frame rate
FPS = 60

def calculate_board_size(rows, cols):
    width = MARGIN * 2 + cols * CARD_SIZE + (cols - 1) * GAP
    height = MARGIN * 2 + rows * CARD_SIZE + (rows - 1) * GAP
    return max(width, 600), max(height, 700)

WIDTH, HEIGHT = calculate_board_size(DEFAULT_ROWS, DEFAULT_COLS)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 200)
GREEN = (50, 200, 100)
RED = (200, 50, 50)
