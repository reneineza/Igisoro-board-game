import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
BACKGROUND_COLOR = (51, 102, 0)
PIT_COLOR = (153, 76, 0)
SEED_COLOR = (255, 204, 0)
FPS = 30

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Igisoro (Mancala)")

# Igisoro board setup
pit_radius = 30
pit_margin = 20
pit_positions = [(pit_margin + i * (2 * pit_radius + pit_margin), HEIGHT // 2) for i in range(6)]
seeds_per_pit = 4
pits = [seeds_per_pit] * 12
player_turn = 0  # 0 for Player A, 1 for Player B

# Fonts
font = pygame.font.Font(None, 36)

# Button and Label setup
button_font = pygame.font.Font(None, 24)
player_labels = [button_font.render("Player A", True, SEED_COLOR),
                 button_font.render("Player B", True, SEED_COLOR)]
player_labels_rects = [player_labels[0].get_rect(center=(WIDTH // 4, HEIGHT - 30)),
                       player_labels[1].get_rect(center=(3 * WIDTH // 4, HEIGHT - 30))]
player_buttons = [pygame.Rect(20, HEIGHT - 50, 120, 40),
                  pygame.Rect(WIDTH - 140, HEIGHT - 50, 120, 40)]
restart_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 50, 120, 40)

def draw_board():
    screen.fill(BACKGROUND_COLOR)
    for i, (x, y) in enumerate(pit_positions):
        pygame.draw.circle(screen, PIT_COLOR, (x, y), pit_radius)
        seeds = pits[i]
        if seeds > 0:
            text = font.render(str(seeds), True, SEED_COLOR)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

    # Draw player labels and buttons
    for i in range(2):
        pygame.draw.rect(screen, SEED_COLOR, player_buttons[i])
        screen.blit(player_labels[i], player_labels_rects[i])

    pygame.display.update()

def distribute_seeds(pit_index):
    seeds = pits[pit_index]
    pits[pit_index] = 0
    while seeds > 0:
        pit_index = (pit_index + 1) % 12
        if player_turn == 0 and pit_index == 6:
            pit_index = (pit_index + 1) % 12
        if player_turn == 1 and pit_index == 0:
            pit_index = (pit_index + 1) % 12
        pits[pit_index] += 1
        seeds -= 1
    return pit_index

def check_game_over():
    player_a_pits = sum(pits[0:6])
    player_b_pits = sum(pits[6:12])
    if player_a_pits == 0 or player_b_pits == 0:
        for i in range(6):
            pits[i] = 0
            pits[i + 6] = 0
        return True
    return False

def show_winner():
    winner = None
    player_a_pits = sum(pits[0:6])
    player_b_pits = sum(pits[6:12])
    if player_a_pits > player_b_pits:
        winner = "Player A"
    elif player_b_pits > player_a_pits:
        winner = "Player B"
    if winner:
        winner_label = font.render(f"{winner} wins!", True, SEED_COLOR)
        winner_rect = winner_label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(winner_label, winner_rect)
        pygame.display.update()

# Game loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if restart_button.collidepoint(x, y):
                pits = [seeds_per_pit] * 12
                player_turn = 0
                game_over = False
            for i, button in enumerate(player_buttons):
                if button.collidepoint(x, y) and player_turn == i:
                    for i, (px, py) in enumerate(pit_positions):
                        if button.collidepoint(px, py) and pits[i] > 0:
                            pit_index = i
                            pit_index = distribute_seeds(pit_index)
                            if check_game_over():
                                game_over = True
                            player_turn = 1 - player_turn  # Switch player turn

    draw_board()
    if game_over:
        show_winner()
    pygame.time.delay(1000 // FPS)

# Quit Pygame
pygame.quit()
sys.exit()
