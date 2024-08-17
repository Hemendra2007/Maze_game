import pygame
import sys
import time
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 20
PLAYER_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)
WALL_COLOR = (255, 0, 0)
GOAL_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 255)
FPS = 60

font = pygame.font.SysFont(None, 48)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
start_time = time.time()

# Static Walls
walls = [
    pygame.Rect(100, 100, 100, 20),
    pygame.Rect(300, 200, 200, 20),
    pygame.Rect(50, 300, 150, 20),
    pygame.Rect(400, 100, 20, 150),
    pygame.Rect(200, 50, 100, 20),
    pygame.Rect(150, 250, 200, 20),
    pygame.Rect(350, 50, 150, 20),
    pygame.Rect(500, 150, 20, 100)
]

# Moving Obstacles
moving_walls = [
    pygame.Rect(150, 150, 20, 80),
    pygame.Rect(450, 250, 20, 80)
]
moving_directions = [1, -1] 

goal = pygame.Rect(500, 350, 40, 40)
score = 0 

clock = pygame.time.Clock()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    # Moving walls logic
    for i, wall in enumerate(moving_walls):
        wall.y += moving_directions[i] * player_speed // 2
        if wall.top <= 0 or wall.bottom >= HEIGHT:
            moving_directions[i] *= -1

    # Collision detection 
    for wall in walls + moving_walls:
        if player_rect.colliderect(wall):
            if keys[pygame.K_LEFT]:
                player_x += player_speed
            if keys[pygame.K_RIGHT]:
                player_x -= player_speed
            if keys[pygame.K_UP]:
                player_y += player_speed
            if keys[pygame.K_DOWN]:
                player_y -= player_speed

    # Check if the player reaches the goal
    if player_rect.colliderect(goal):
        elapsed_time = time.time() - start_time
        score += int(1000 / elapsed_time)  
        screen.fill(BG_COLOR)
        draw_text(f"You Win! Score: {score}", font, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    screen.fill(BG_COLOR)

    # walls
    for wall in walls + moving_walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)

    # player and goal
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    pygame.draw.rect(screen, GOAL_COLOR, goal)

    # timer and score
    elapsed_time = time.time() - start_time
    draw_text(f"Time: {int(elapsed_time)}s | Score: {score}", font, TEXT_COLOR, screen, 150, 20)

    pygame.display.flip()
    clock.tick(FPS)
