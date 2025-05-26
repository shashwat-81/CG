import pygame
import random
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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

# Initialize Pygame and OpenGL
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("Racing Gems - Trees Only (OpenGL)")
clock = pygame.time.Clock()
glutInit()

# Colors as normalized OpenGL floats
DARK_GREY = (77/255, 77/255, 77/255)
WHITE = (1, 1, 1)
BLUE = (0, 0, 1)
RED = (1, 0, 0)
YELLOW = (1, 1, 0)
BLACK = (0, 0, 0)
WINDOW_BLUE = (180/255, 240/255, 255/255)
GRASS_GREEN = (50/255, 168/255, 82/255)
SIDEWALK_GRAY = (169/255, 169/255, 169/255)
TREE_BARK = (101/255, 67/255, 33/255)
TREE_LEAVES_DARK = (34/255, 139/255, 34/255)
TREE_LEAVES_LIGHT = (50/255, 205/255, 50/255)

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
    
    def draw_tree(self):
        # Draw tree trunk with shadow
        trunk_width = self.width // 5
        trunk_height = self.height // 3
        trunk_x = self.x + (self.width - trunk_width) // 2
        trunk_y = self.y + self.height - trunk_height

        # Shadow trunk
        draw_rect_gl(trunk_x+3, trunk_y+3, trunk_width, trunk_height, (20/255, 20/255, 20/255))
        draw_rect_gl(trunk_x, trunk_y, trunk_width, trunk_height, TREE_BARK)
        
        # Draw tree leaves (triangle) with leaf color variation
        leaf_color = TREE_LEAVES_DARK if self.variation == 0 else TREE_LEAVES_LIGHT
        points = [(self.x, trunk_y), (self.x + self.width // 2, self.y), (self.x + self.width, trunk_y)]

        # Shadow leaves
        shadow_points = [(x+3, y+3) for x, y in points]
        draw_triangle_gl(shadow_points, (20/255, 20/255, 20/255))
        draw_triangle_gl(points, leaf_color)

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

def draw_rect_gl(x, y, width, height, color):
    """Draw rectangle using OpenGL with screen coords."""
    glColor3f(*color)
    # Convert to OpenGL coords
    x1 = (x / WINDOW_WIDTH) * 2 - 1
    y1 = 1 - (y / WINDOW_HEIGHT) * 2
    x2 = ((x + width) / WINDOW_WIDTH) * 2 - 1
    y2 = 1 - ((y + height) / WINDOW_HEIGHT) * 2

    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_triangle_gl(points, color):
    glColor3f(*color)
    glBegin(GL_TRIANGLES)
    for (x, y) in points:
        x_gl = (x / WINDOW_WIDTH) * 2 - 1
        y_gl = 1 - (y / WINDOW_HEIGHT) * 2
        glVertex2f(x_gl, y_gl)
    glEnd()

def draw_car(x, y, color):
    # Car Body
    draw_rect_gl(x, y, CAR_WIDTH, CAR_HEIGHT, color)

    # Windows
    draw_rect_gl(x + 10, y + 10, 30, 20, WINDOW_BLUE)   # Left window
    draw_rect_gl(x + 10, y + 40, 30, 20, WINDOW_BLUE)   # Right window
    draw_rect_gl(x + 5, y + 70, 40, 20, WINDOW_BLUE)    # Windshield

    # Wheels
    draw_rect_gl(x - 5, y + 10, 10, 20, BLACK)  # Front-left
    draw_rect_gl(x + CAR_WIDTH - 5, y + 10, 10, 20, BLACK)  # Front-right
    draw_rect_gl(x - 5, y + CAR_HEIGHT - 30, 10, 20, BLACK)  # Rear-left
    draw_rect_gl(x + CAR_WIDTH - 5, y + CAR_HEIGHT - 30, 10, 20, BLACK)  # Rear-right

    # Headlights
    draw_rect_gl(x + 5, y + CAR_HEIGHT - 5, 10, 5, YELLOW)
    draw_rect_gl(x + CAR_WIDTH - 15, y + CAR_HEIGHT - 5, 10, 5, YELLOW)

def draw_road():
    # Grass on sides
    draw_rect_gl(0, 0, 100, WINDOW_HEIGHT, GRASS_GREEN)
    draw_rect_gl(500, 0, 100, WINDOW_HEIGHT, GRASS_GREEN)
    
    # Sidewalks between grass and road
    draw_rect_gl(100, 0, 15, WINDOW_HEIGHT, SIDEWALK_GRAY)
    draw_rect_gl(485, 0, 15, WINDOW_HEIGHT, SIDEWALK_GRAY)
    
    # Road
    draw_rect_gl(115, 0, 370, WINDOW_HEIGHT, DARK_GREY)
    
    # Lane markings
    for y in range(0, WINDOW_HEIGHT, 80):
        draw_rect_gl(195, y, 10, 40, WHITE)
        draw_rect_gl(295, y, 10, 40, WHITE)
        draw_rect_gl(395, y, 10, 40, WHITE)

def check_collision(car_x, car_y, enemy_x, enemy_y):
    return not (car_x + CAR_WIDTH < enemy_x or car_x > enemy_x + CAR_WIDTH or
                car_y + CAR_HEIGHT < enemy_y or car_y > enemy_y + CAR_HEIGHT)

def draw_scenery():
    for tree in left_trees:
        tree.draw_tree()
    for tree in right_trees:
        tree.draw_tree()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1,1,0)):
    """Draw text at normalized coords x,y in OpenGL (-1 to 1)."""
    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

def main():
    global car_pos_x, car_pos_y, score, game_over, is_paused, ENEMY_BASE_SPEED
    
    reset_game()
    running = True

    while running:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if not game_over and not is_paused:
            if keys[pygame.K_LEFT]:
                car_pos_x = max(100, car_pos_x - car_speed)
            if keys[pygame.K_RIGHT]:
                car_pos_x = min(450 - CAR_WIDTH, car_pos_x + car_speed)
            if keys[pygame.K_UP]:
                car_pos_y = max(0, car_pos_y - car_speed)
            if keys[pygame.K_DOWN]:
                car_pos_y = min(WINDOW_HEIGHT - CAR_HEIGHT, car_pos_y + car_speed)

        if keys[pygame.K_p]:
            is_paused = not is_paused
            pygame.time.wait(300)  # Prevent rapid toggle

        if keys[pygame.K_r] and game_over:
            reset_game()

        # Draw static environment
        draw_road()
        draw_scenery()

        if not game_over and not is_paused:
            # Move and draw enemies
            for enemy in enemies:
                enemy.y += enemy.speed
                if enemy.y > WINDOW_HEIGHT:
                    enemy.x = 150 + (random.randint(0, 3) * LANE_WIDTH)
                    enemy.y = -CAR_HEIGHT
                    enemy.speed = ENEMY_BASE_SPEED + random.randint(0, 2)
                    score += 1

                    # Increase difficulty every 10 points
                    if score % 10 == 0:
                        ENEMY_BASE_SPEED += 1

                draw_car(enemy.x, enemy.y, RED)

                if check_collision(car_pos_x, car_pos_y, enemy.x, enemy.y):
                    game_over = True

            # Win condition - check if player reached the top
            if car_pos_y <= 0:
                game_over = True
                score = 100  # Set score to 100 to trigger win message

            # Draw player car
            draw_car(car_pos_x, car_pos_y, BLUE)
        else:
            # Draw stationary enemies
            for enemy in enemies:
                draw_car(enemy.x, enemy.y, RED)
            draw_car(car_pos_x, car_pos_y, BLUE)

        # Draw UI text
        # Position text near top-left corner: convert pixel to normalized (-1 to 1)
        draw_text(-0.95, 0.9, f"Score: {score}", color=YELLOW)

        if is_paused:
            draw_text(-0.25, 0, "PAUSED - Press P to resume", color=YELLOW)

        if game_over:
            draw_text(-0.2, 0.2, "GAME OVER", color=RED)
            draw_text(-0.45, 0, "Press R to restart", color=YELLOW)
            if score >= 100:
                draw_text(-0.25, -0.2, "YOU WIN!", color=YELLOW)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
