import pygame
import sys
from settings import WIDTH, HEIGHT, FPS, WHITE, BLUE, calculate_board_size
from board import Board
from assets import load_assets
from ui import draw_board, draw_ui, draw_menu, draw_gameover

# Initialize pygame and create a window.
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Matching Game")
clock = pygame.time.Clock()

# Load assets (fonts, sounds, images).
assets = load_assets()

# Define game states.
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"

# Global variables for game state.
game_state = STATE_MENU
grid_size = (4, 4)  # Default grid size (can be changed via the menu)
board = None
flipping_cards = {}
start_time = 0
time_limit = 60000  # Default time limit in milliseconds (will be updated)
player_won = False

def start_new_game():
    global board, flipping_cards, start_time, WIDTH, HEIGHT, grid_size, screen, time_limit
    ROWS, COLS = grid_size
    WIDTH, HEIGHT = calculate_board_size(ROWS, COLS)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    board = Board(ROWS, COLS)
    flipping_cards = {}
    start_time = pygame.time.get_ticks()
    # Set time limit based on board size:
    # For 3x4 → 45 sec, for 4x4 → 75 sec, for 4x5 → 120 sec.
    if grid_size == (3, 4):
        time_limit = 45 * 1000
    elif grid_size == (4, 4):
        time_limit = 75 * 1000
    elif grid_size == (4, 5):
        time_limit = 120 * 1000
    else:
        time_limit = 60 * 1000  # Fallback

while True:
    if game_state == STATE_MENU:
        # Display the menu and get the grid size from the user.
        grid_size = draw_menu(screen, assets)
        start_new_game()
        game_state = STATE_PLAYING

    elif game_state == STATE_PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                board.handle_click(mx, my, flipping_cards, assets)
            elif event.type == pygame.USEREVENT:
                board.check_match(assets)
                pygame.time.set_timer(pygame.USEREVENT, 0)

        # Update flip animations.
        for key in list(flipping_cards.keys()):
            flipping_cards[key] += 0.05
            if flipping_cards[key] >= 1.0:
                del flipping_cards[key]

        screen.fill(WHITE)
        draw_board(screen, board, assets, flipping_cards)
        # Pass the time limit so that UI shows remaining time.
        draw_ui(screen, board, assets, start_time, time_limit)

        # Check for win or if time is up.
        elapsed = pygame.time.get_ticks() - start_time
        if board.check_win():
            if assets["sounds"].get("win"):
                assets["sounds"]["win"].play()
            player_won = True
            game_state = STATE_GAMEOVER
        elif elapsed >= time_limit:
            if assets["sounds"].get("gameover"):
                assets["sounds"]["gameover"].play()
            player_won = False
            game_state = STATE_GAMEOVER

        pygame.display.flip()
        clock.tick(FPS)

    elif game_state == STATE_GAMEOVER:
        # Show game over screen; pass win/lose flag.
        choice = draw_gameover(screen, board, assets, start_time, player_won)
        if choice == "restart":
            game_state = STATE_MENU
        elif choice == "quit":
            pygame.quit()
            sys.exit()
