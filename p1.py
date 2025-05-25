import pygame
import random
import sys

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
CAR_WIDTH = 50
CAR_HEIGHT = 100
LANE_WIDTH = 100
MAX_ENEMIES = 3
ENEMY_BASE_SPEED = 5

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Racing Gems - Realistic Car Version")
clock = pygame.time.Clock()

# Colors
DARK_GREY = (77, 77, 77)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WINDOW_BLUE = (180, 240, 255)

# Game variables
car_pos_x = 250
car_pos_y = WINDOW_HEIGHT - CAR_HEIGHT
car_speed = 20
score = 0
game_over = False
is_paused = False

# Enemy structure
class Enemy:
    def __init__(self):
        self.x = 150 + (random.randint(0, 3) * LANE_WIDTH)
        self.y = WINDOW_HEIGHT + random.randint(0, 300)
        self.speed = ENEMY_BASE_SPEED + random.randint(0, 2)

enemies = [Enemy() for _ in range(MAX_ENEMIES)]

def reset_game():
    global car_pos_x, car_pos_y, score, game_over, is_paused
    car_pos_x = 250
    car_pos_y = WINDOW_HEIGHT - CAR_HEIGHT
    score = 0
    game_over = False
    is_paused = False
    reset_enemies()

def reset_enemies():
    global enemies
    enemies = [Enemy() for _ in range(MAX_ENEMIES)]

def draw_text(text, x, y, font_size=30, color=WHITE):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_rect(x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))

def draw_car(x, y, color):
    # Car Body
    draw_rect(x, y, CAR_WIDTH, CAR_HEIGHT, color)

    # Windows
    draw_rect(x + 10, y + 10, 30, 20, WINDOW_BLUE)   # Left window
    draw_rect(x + 10, y + 40, 30, 20, WINDOW_BLUE)   # Right window
    draw_rect(x + 5, y + 70, 40, 20, WINDOW_BLUE)    # Windshield

    # Wheels
    draw_rect(x - 5, y + 10, 10, 20, BLACK)  # Front-left
    draw_rect(x + CAR_WIDTH - 5, y + 10, 10, 20, BLACK)  # Front-right
    draw_rect(x - 5, y + CAR_HEIGHT - 30, 10, 20, BLACK)  # Rear-left
    draw_rect(x + CAR_WIDTH - 5, y + CAR_HEIGHT - 30, 10, 20, BLACK)  # Rear-right

    # Headlights
    draw_rect(x + 5, y + CAR_HEIGHT - 5, 10, 5, YELLOW)
    draw_rect(x + CAR_WIDTH - 15, y + CAR_HEIGHT - 5, 10, 5, YELLOW)

def draw_road():
    pygame.draw.rect(screen, DARK_GREY, (100, 0, 400, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (195, y, 10, 40))
        pygame.draw.rect(screen, WHITE, (295, y, 10, 40))
        pygame.draw.rect(screen, WHITE, (395, y, 10, 40))

def check_collision(car_x, car_y, enemy_x, enemy_y):
    return not (car_x + CAR_WIDTH < enemy_x or car_x > enemy_x + CAR_WIDTH or
                car_y + CAR_HEIGHT < enemy_y or car_y > enemy_y + CAR_HEIGHT)

def main():
    global car_pos_x, car_pos_y, car_speed, game_over, is_paused, score
    global ENEMY_BASE_SPEED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    reset_game()
                if event.key == pygame.K_p:
                    is_paused = not is_paused
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not game_over and not is_paused:
            keys = pygame.key.get_pressed()

            # Horizontal movement
            if keys[pygame.K_LEFT] and car_pos_x > 150:
                car_pos_x -= car_speed
            if keys[pygame.K_RIGHT] and car_pos_x < 450:
                car_pos_x += car_speed

            # Vertical movement
            if keys[pygame.K_UP] and car_pos_y > 0:
                car_pos_y -= car_speed
            if keys[pygame.K_DOWN] and car_pos_y < WINDOW_HEIGHT - CAR_HEIGHT:
                car_pos_y += car_speed

            # Clamp within screen
            car_pos_x = max(150, min(car_pos_x, 450))
            car_pos_y = max(0, min(car_pos_y, WINDOW_HEIGHT - CAR_HEIGHT))

            for enemy in enemies:
                enemy.y += enemy.speed
                if enemy.y > WINDOW_HEIGHT:
                    enemy.y = -CAR_HEIGHT
                    enemy.x = 150 + (random.randint(0, 3) * LANE_WIDTH)
                    enemy.speed = ENEMY_BASE_SPEED + random.randint(0, 2)
                    score += 1
                    if score % 10 == 0:
                        ENEMY_BASE_SPEED += 1

                if check_collision(car_pos_x, car_pos_y, enemy.x, enemy.y):
                    game_over = True

            screen.fill((112, 128, 144))  # Background
            draw_road()
            draw_car(car_pos_x, car_pos_y, BLUE)

            for enemy in enemies:
                draw_car(enemy.x, enemy.y, RED)

            draw_text(f"Score: {score}", 10, 770, font_size=30, color=YELLOW)

            if car_pos_y <= 0:
                game_over = True
                draw_text("YOU WIN!", 230, 400, font_size=50, color=YELLOW)

        else:
            screen.fill((112, 128, 144))
            if car_pos_y <= 0:
                draw_text("YOU WIN!", 230, 400, font_size=50, color=YELLOW)
            else:
                draw_text("GAME OVER", 220, 400, font_size=50, color=RED)
            draw_text(f"Final Score: {score}", 210, 360, font_size=30, color=YELLOW)
            draw_text("Press 'R' to Restart", 160, 320, font_size=30, color=WHITE)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    reset_game()
    main()
