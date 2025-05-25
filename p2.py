import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import time

# Game config
NUM_TARGETS = 5
TIME_LIMIT = 30  # seconds
ROCKET_SPEED = 0.05
TARGET_RADIUS = 0.1

# Game state
rocket_x, rocket_y = 0.0, -1.5
rocket_angle = 90
launched = False
start_time = None
targets = []
hit_targets = []

def generate_targets():
    global targets
    targets = []
    while len(targets) < NUM_TARGETS:
        x = random.uniform(-1.8, 1.8)
        y = random.uniform(-1.0, 1.8)
        targets.append((x, y))

def draw_circle(x, y, radius):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for angle in range(0, 361, 10):
        rad = math.radians(angle)
        glVertex2f(x + math.cos(rad) * radius, y + math.sin(rad) * radius)
    glEnd()

def draw_targets():
    for tx, ty in targets:
        if (tx, ty) not in hit_targets:
            glColor3f(0, 1, 0)
            draw_circle(tx, ty, TARGET_RADIUS)

def draw_rocket():
    glPushMatrix()
    glTranslatef(rocket_x, rocket_y, 0)
    glRotatef(rocket_angle - 90, 0, 0, 1)
    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)
    glVertex2f(-0.05, 0)
    glVertex2f(0.05, 0)
    glVertex2f(0.05, 0.4)
    glVertex2f(-0.05, 0.4)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 0)
    glVertex2f(-0.05, 0.4)
    glVertex2f(0.05, 0.4)
    glVertex2f(0.0, 0.55)
    glEnd()
    glPopMatrix()

def move_rocket():
    global rocket_x, rocket_y
    dx = ROCKET_SPEED * math.cos(math.radians(rocket_angle))
    dy = ROCKET_SPEED * math.sin(math.radians(rocket_angle))
    rocket_x += dx
    rocket_y += dy

def check_hit():
    global hit_targets
    for tx, ty in targets:
        if (tx, ty) not in hit_targets:
            dist = math.sqrt((rocket_x - tx)**2 + (rocket_y - ty)**2)
            if dist < TARGET_RADIUS + 0.08:
                hit_targets.append((tx, ty))
                reset_rocket()

def reset_rocket():
    global rocket_x, rocket_y, launched, rocket_angle
    rocket_x, rocket_y = 0.0, -1.5
    rocket_angle = 90
    launched = False

def restart_game():
    global hit_targets, start_time, win, lose
    hit_targets.clear()
    reset_rocket()
    generate_targets()
    start_time = time.time()
    win = False
    lose = False
    pygame.display.set_caption("🚀 Rocket Target Game")

def main():
    global rocket_angle, launched, start_time, win, lose

    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(-2, 2, -2, 2)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)

    generate_targets()
    reset_rocket()
    start_time = time.time()
    win = False
    lose = False

    game_running = True

    while game_running:
        glClear(GL_COLOR_BUFFER_BIT)
        clock.tick(60)

        # Time logic
        elapsed = time.time() - start_time
        time_left = max(0, TIME_LIMIT - int(elapsed))

        for event in pygame.event.get():
            if event.type == QUIT:
                game_running = False

        keys = pygame.key.get_pressed()
        if not win and not lose:
            if keys[K_LEFT]:
                rocket_angle += 3
            if keys[K_RIGHT]:
                rocket_angle -= 3
            if keys[K_SPACE] and not launched:
                launched = True

        if (win or lose) and keys[K_r]:
            restart_game()

        # Move rocket and check for hits
        if launched and not win and not lose:
            move_rocket()
            check_hit()

            if abs(rocket_x) > 2 or abs(rocket_y) > 2:
                reset_rocket()

        # Game win/lose logic
        if len(hit_targets) == NUM_TARGETS and not win:
            win = True
            launched = False
            pygame.display.set_caption("🏆 You Win! Press R to Restart")

        if time_left == 0 and not win and not lose:
            lose = True
            launched = False
            pygame.display.set_caption("💥 Time's Up! Press R to Restart")

        # Drawing
        draw_rocket()
        draw_targets()

        # Timer and score display
        surface = font.render(f"Time Left: {time_left}s  |  Hits: {len(hit_targets)}/{NUM_TARGETS}", True, (255, 255, 255))
        screen.blit(surface, (20, 20))

        if win:
            win_surface = font.render("🏆 You Win! Press R to Restart", True, (255, 255, 0))
            screen.blit(win_surface, (200, 300))
        elif lose:
            lose_surface = font.render("💥 You Lose! Press R to Restart", True, (255, 0, 0))
            screen.blit(lose_surface, (200, 300))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
