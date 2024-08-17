import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 20
PLAYER_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)
WALL_COLOR = (255, 0, 0)
GOAL_COLOR = (0, 0, 255)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5

# Walls and Goal
walls = [
    pygame.Rect(100, 100, 100, 20),
    pygame.Rect(300, 200, 200, 20),
    pygame.Rect(50, 300, 150, 20),
    pygame.Rect(400, 100, 20, 150),
    pygame.Rect(200, 50, 100, 20)
]
goal = pygame.Rect(500, 350, 40, 40)

clock = pygame.time.Clock()
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

    for wall in walls:
        if player_rect.colliderect(wall):
            if keys[pygame.K_LEFT]:
                player_x += player_speed
            if keys[pygame.K_RIGHT]:
                player_x -= player_speed
            if keys[pygame.K_UP]:
                player_y += player_speed
            if keys[pygame.K_DOWN]:
                player_y -= player_speed

    if player_rect.colliderect(goal):
        print("You Win!")
        pygame.quit()
        sys.exit()

    screen.fill(BG_COLOR)
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    pygame.draw.rect(screen, GOAL_COLOR, goal)
    
    pygame.display.flip()
    clock.tick(FPS)
