import pygame
from settings import CARD_SIZE, GAP, MARGIN, WIDTH, HEIGHT

# Define our new color palette:
BACKGROUND_COLOR = (220, 240, 255)    # Light, white-blue background.
DEEP_BLUE      = (0, 51, 102)         # Deep blue for texts.
OPTION_COLOR   = (0, 102, 204)        # Blue for options (normal state).
OPTION_HOVER   = (0, 70, 140)         # Darker blue for options when hovered.
WHITE          = (255, 255, 255)
GREEN          = (50, 200, 100)
BLUE           = (50, 100, 200)        # Card back color.
RED            = (200, 50, 50)

def draw_board(screen, board, assets, flipping_cards):
    # Fill the background with our light blue.
    screen.fill(BACKGROUND_COLOR)
    
    for row in board.cards:
        for card in row:
            x, y = card.x, card.y
            flip_progress = flipping_cards.get((card.row, card.col), 1 if card.revealed else 0)

            # Draw a shadow behind the card.
            shadow_offset = 5
            shadow_rect = pygame.Rect(x + shadow_offset, y + shadow_offset, CARD_SIZE, CARD_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=10)
            
            if flip_progress < 1:
                # Card back flip animation (simulate shrink effect).
                width = int(CARD_SIZE * (1 - flip_progress))
                card_back_rect = pygame.Rect(x + (CARD_SIZE - width) // 2, y, width, CARD_SIZE)
                pygame.draw.rect(screen, BLUE, card_back_rect, border_radius=10)
            else:
                if card.revealed or card.matched:
                    # Draw a border indicating a revealed or matched card.
                    border_color = GREEN if card.matched else WHITE
                    card_rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
                    pygame.draw.rect(screen, border_color, card_rect, border_radius=10)
                    # Draw an inner, slightly smaller rectangle for a padded look.
                    inner_rect = pygame.Rect(x + 5, y + 5, CARD_SIZE - 10, CARD_SIZE - 10)
                    pygame.draw.rect(screen, (240, 240, 240), inner_rect, border_radius=8)
                    
                    # Draw the image on the card.
                    image_key = card.value  # e.g., "apple"
                    if image_key in assets.get("images", {}):
                        screen.blit(assets["images"][image_key], (x, y))
                    else:
                        # Fallback: draw text in deep blue if image not available.
                        font_size = max(20, CARD_SIZE // 3)
                        font = pygame.font.Font(None, font_size)
                        text = font.render(image_key, True, DEEP_BLUE)
                        screen.blit(
                            text,
                            (x + CARD_SIZE // 2 - text.get_width() // 2,
                             y + CARD_SIZE // 2 - text.get_height() // 2)
                        )
                else:
                    # Draw the card back.
                    pygame.draw.rect(screen, BLUE, (x, y, CARD_SIZE, CARD_SIZE), border_radius=10)

def draw_ui(screen, board, assets, start_time, time_limit):
    # Instead of drawing a dark panel, we remove it so the texts are drawn directly.
    # ui_height = HEIGHT // 10  # Not used for panel background now.
    
    font = assets["font"]
    # Draw the Matches and Time texts with a small margin from the top.
    moves_text = font.render(f"Matches: {board.score}", True, DEEP_BLUE)
    screen.blit(moves_text, (10, 10))
    
    elapsed = pygame.time.get_ticks() - start_time
    remaining = max(0, (time_limit - elapsed) // 1000)
    timer_text = font.render(f"Time: {remaining}s", True, DEEP_BLUE)
    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

def draw_menu(screen, assets):
    """Display a polished main menu and return the chosen grid size."""
    screen.fill(BACKGROUND_COLOR)
    
    font = pygame.font.Font(None, 60)
    title_text = font.render("Memory Matching Game", True, DEEP_BLUE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 5))
    
    modes = {"3x4": (3, 4), "4x4": (4, 4), "4x5": (4, 5)}
    button_w, button_h = 220, 70
    button_x = WIDTH // 2 - button_w // 2
    button_y_start = HEIGHT // 2 - 100
    button_gap = 90
    
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill(BACKGROUND_COLOR)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 5))
        
        for idx, (mode, size) in enumerate(modes.items()):
            button_y = button_y_start + idx * button_gap
            button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
            # Use our blue options for buttons.
            if button_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, OPTION_HOVER, button_rect, border_radius=12)
            else:
                pygame.draw.rect(screen, OPTION_COLOR, button_rect, border_radius=12)
            mode_text = font.render(mode, True, DEEP_BLUE)
            screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, button_y + 15))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, (mode, size) in enumerate(modes.items()):
                    button_y = button_y_start + idx * button_gap
                    button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        return size

def draw_gameover(screen, board, assets, start_time, player_won):
    """Display an enhanced game over screen and return the player's choice ('restart' or 'quit')."""
    screen.fill(BACKGROUND_COLOR)
    
    font = pygame.font.Font(None, 60)
    if player_won:
        result_text = font.render(f"You Win! Matches: {board.score}", True, DEEP_BLUE)
    else:
        result_text = font.render("Time's Up! You Lose!", True, RED)
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 3))
    
    restart_text = font.render("Play Again", True, DEEP_BLUE)
    quit_text = font.render("Quit", True, DEEP_BLUE)
    
    button_w, button_h = 220, 70
    button_x = WIDTH // 2 - button_w // 2
    button_y_restart = HEIGHT // 2
    button_y_quit = HEIGHT // 2 + 90
    
    while True:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 3))
        # Draw the restart button.
        restart_rect = pygame.Rect(button_x, button_y_restart, button_w, button_h)
        pygame.draw.rect(screen, OPTION_COLOR, restart_rect, border_radius=12)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, button_y_restart + 15))
        # Draw the quit button.
        quit_rect = pygame.Rect(button_x, button_y_quit, button_w, button_h)
        pygame.draw.rect(screen, OPTION_COLOR, quit_rect, border_radius=12)
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, button_y_quit + 15))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mx, my):
                    return "restart"
                if quit_rect.collidepoint(mx, my):
                    return "quit"
