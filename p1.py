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

TREE_WIDTH = 40
TREE_HEIGHT = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Racing Gems - Trees Only")
clock = pygame.time.Clock()

# Colors
DARK_GREY = (77, 77, 77)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WINDOW_BLUE = (180, 240, 255)
GRASS_GREEN = (50, 168, 82)
SIDEWALK_GRAY = (169, 169, 169)
TREE_BARK = (101, 67, 33)
TREE_LEAVES_DARK = (34, 139, 34)
TREE_LEAVES_LIGHT = (50, 205, 50)

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

# Scenery Objects for Trees
class SceneryObject:
    def __init__(self, x, y, width, height, color, variation=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.variation = variation  # For tree leaf color variation
    
    def draw_tree(self, surface):
        # Draw tree trunk with shadow
        trunk_width = self.width // 5
        trunk_height = self.height // 3
        trunk_x = self.x + (self.width - trunk_width) // 2
        trunk_y = self.y + self.height - trunk_height

        # Shadow trunk
        pygame.draw.rect(surface, (20, 20, 20), (trunk_x+3, trunk_y+3, trunk_width, trunk_height))
        pygame.draw.rect(surface, TREE_BARK, (trunk_x, trunk_y, trunk_width, trunk_height))
        
        # Draw tree leaves (triangle) with leaf color variation
        leaf_color = TREE_LEAVES_DARK if self.variation == 0 else TREE_LEAVES_LIGHT
        points = [(self.x, trunk_y), (self.x + self.width // 2, self.y), (self.x + self.width, trunk_y)]

        # Shadow leaves
        shadow_points = [(x+3, y+3) for x, y in points]
        pygame.draw.polygon(surface, (20, 20, 20), shadow_points)
        pygame.draw.polygon(surface, leaf_color, points)

# Static scenery positions (trees only)
left_trees = [
    SceneryObject(20, i * 140 + 60, TREE_WIDTH, TREE_HEIGHT, TREE_LEAVES_DARK, variation=i % 2) 
    for i in range(6)
]
right_trees = [
    SceneryObject(540, i * 140 + 100, TREE_WIDTH, TREE_HEIGHT, TREE_LEAVES_DARK, variation=(i + 1) % 2) 
    for i in range(6)
]

def reset_game():
    global car_pos_x, car_pos_y, score, game_over, is_paused, ENEMY_BASE_SPEED
    car_pos_x = 250
    car_pos_y = WINDOW_HEIGHT - CAR_HEIGHT
    score = 0
    game_over = False
    is_paused = False
    reset_enemies()
    ENEMY_BASE_SPEED = 5

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
    # Grass on sides
    pygame.draw.rect(screen, GRASS_GREEN, (0, 0, 100, WINDOW_HEIGHT))
    pygame.draw.rect(screen, GRASS_GREEN, (500, 0, 100, WINDOW_HEIGHT))
    
    # Sidewalks between grass and road
    pygame.draw.rect(screen, SIDEWALK_GRAY, (100, 0, 15, WINDOW_HEIGHT))
    pygame.draw.rect(screen, SIDEWALK_GRAY, (485, 0, 15, WINDOW_HEIGHT))
    
    # Road
    pygame.draw.rect(screen, DARK_GREY, (115, 0, 370, WINDOW_HEIGHT))
    
    # Lane markings
    for y in range(0, WINDOW_HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (195, y, 10, 40))
        pygame.draw.rect(screen, WHITE, (295, y, 10, 40))
        pygame.draw.rect(screen, WHITE, (395, y, 10, 40))

def check_collision(car_x, car_y, enemy_x, enemy_y):
    return not (car_x + CAR_WIDTH < enemy_x or car_x > enemy_x + CAR_WIDTH or
                car_y + CAR_HEIGHT < enemy_y or car_y > enemy_y + CAR_HEIGHT)

def draw_scenery():
    for tree in left_trees:
        tree.draw_tree(screen)
    for tree in right_trees:
        tree.draw_tree(screen)

def main():
    global car_pos_x, car_pos_y, car_speed, game_over, is_paused, score, ENEMY_BASE_SPEED

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

            # Move enemies
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

            # Win condition
            if car_pos_y <= 0:
                game_over = True

        # Drawing
        screen.fill((112, 128, 144))  # Background
        draw_road()
        draw_scenery()
        draw_car(car_pos_x, car_pos_y, BLUE)

        for enemy in enemies:
            draw_car(enemy.x, enemy.y, RED)

        draw_text(f"Score: {score}", 10, 770, font_size=30, color=YELLOW)

        if game_over:
            if car_pos_y <= 0:
                draw_text("YOU WIN!", 230, 400, font_size=50, color=YELLOW)
            else:
                draw_text("GAME OVER", 220, 400, font_size=50, color=RED)
            draw_text(f"Final Score: {score}", 210, 360, font_size=30, color=WHITE)
            draw_text("Press R to Restart", 200, 450, font_size=30, color=WHITE)

        if is_paused and not game_over:
            draw_text("PAUSED", 260, 400, font_size=50, color=YELLOW)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
