import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 20
PLAYER_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5

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

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
    pygame.display.flip()
    
    clock.tick(FPS)
