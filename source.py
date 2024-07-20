import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT_NAME = 'arial'
HIGH_SCORE_FILE = 'highscore.txt'

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Werewolf")

# Load images and resize to 20x20
player_img = pygame.transform.scale(pygame.image.load('player.png'), (60, 60))
enemy_img = pygame.transform.scale(pygame.image.load('enemy.png'), (80, 80))
shield_img = pygame.transform.scale(pygame.image.load('shield.png'), (60, 60))

# Load sounds
collision_sound = pygame.mixer.Sound('collision.mp3')
powerup_sound = pygame.mixer.Sound('jump.mp3')

# Fonts
def get_font(size):
    return pygame.font.Font(pygame.font.match_font(FONT_NAME), size)

def draw_text(surf, text, size, x, y):
    font = get_font(size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Load high score
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read())
    except:
        return 0

# Save high score
def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))

high_score = load_high_score()

# Main menu
def main_menu():
    menu = True
    speed_level = 1
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop(speed_level)
                elif event.key == pygame.K_h:
                    show_high_scores()
                elif event.key == pygame.K_i:
                    show_instructions()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    speed_level = int(event.unicode)

        screen.fill(BLACK)
        draw_text(screen, "Space Werewolf", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        draw_text(screen, "Use Arrow Keys to Select Level", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_text(screen, "Press ENTER to start", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30)
        draw_text(screen, "Press H for High Scores", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60)
        draw_text(screen, "Press I for Instructions", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 90)
        draw_text(screen, f"Selected Level: {speed_level}", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120)
        pygame.display.flip()

# Game loop
def game_loop(speed_level):
    running = True
    score = 0
    shield_active = False
    shield_end_time = 0

    # Game objects and variables
    player = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, 20, 20)
    enemies = [pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), random.randint(-150, -50), 20, 20) for _ in range(5)]
    enemy_speed = speed_level * 2

    # Shield power-up
    shield_powerup = pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), random.randint(-150, -50), 20, 20)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
            player.move_ip(5, 0)

        # Move enemies
        for enemy in enemies:
            enemy.move_ip(0, enemy_speed)
            if enemy.top > SCREEN_HEIGHT:
                enemy.top = random.randint(-150, -50)
                enemy.left = random.randint(0, SCREEN_WIDTH - 20)
                score += 1

        # Move shield power-up
        shield_powerup.move_ip(0, 3)
        if shield_powerup.top > SCREEN_HEIGHT:
            shield_powerup.top = random.randint(-150, -50)
            shield_powerup.left = random.randint(0, SCREEN_WIDTH - 20)

        # Check collisions
        if not shield_active and any(player.colliderect(enemy) for enemy in enemies):
            collision_sound.play()
            running = False

        # Check if player picks up shield power-up
        if player.colliderect(shield_powerup):
            powerup_sound.play()
            shield_active = True
            shield_end_time = time.time() + 5
            shield_powerup.top = random.randint(-150, -50)
            shield_powerup.left = random.randint(0, SCREEN_WIDTH - 20)

        # Check if shield is active
        if shield_active and time.time() > shield_end_time:
            shield_active = False

        # Drawing
        screen.fill(BLACK)
        screen.blit(player_img, player.topleft)
        for enemy in enemies:
            screen.blit(enemy_img, enemy.topleft)
        screen.blit(shield_img, shield_powerup.topleft)
        if shield_active:
            screen.blit(shield_img, player.topleft)
        draw_text(screen, f"Score: {score}", 22, 70, 10)
        pygame.display.flip()

    # Check if high score is beaten
    if score > high_score:
        save_high_score(score)

# Show high scores
def show_high_scores():
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show = False

        screen.fill(BLACK)
        draw_text(screen, "High Scores", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        draw_text(screen, f"High Score: {high_score}", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_text(screen, "Press ENTER to return to the main menu", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
        pygame.display.flip()

# Show instructions
def show_instructions():
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show = False

        screen.fill(BLACK)
        draw_text(screen, "Instructions", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        draw_text(screen, "Use arrow keys to move", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_text(screen, "Avoid the enemies!", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30)
        draw_text(screen, "Collect shields for invincibility", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60)
        draw_text(screen, "Press ENTER to return to the main menu", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
