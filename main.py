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
GOAL_COLORS = [(0, 0, 255), (255, 255, 0), (0, 255, 255)]
POWERUP_COLOR = (255, 165, 0)  # Orange
ENEMY_COLOR = (255, 105, 180)  # Hot pink
TEXT_COLOR = (255, 255, 255)
FPS = 60

font = pygame.font.SysFont(None, 48)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
start_time = time.time()
lives = 3
powerup_duration = 5  # Duration of speed boost in seconds
powerup_timer = 0

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
moving_speeds = [random.randint(2, 5) for _ in moving_walls]

# Goals
goals = [
    pygame.Rect(500, 350, 40, 40),
    pygame.Rect(200, 150, 40, 40),
    pygame.Rect(350, 300, 40, 40)
]
goal_colors = GOAL_COLORS[:len(goals)]

# Power-ups
powerups = [pygame.Rect(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), 20, 20) for _ in range(2)]

# Enemies
enemies = [
    pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 20, 20),
    pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 20, 20)
]
enemy_speeds = [2, 2]

score = 0
level = 1
clock = pygame.time.Clock()
pause = False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def reset_game():
    global player_x, player_y, start_time, moving_walls, moving_directions, moving_speeds, level, player_speed, walls, goals, goal_colors, lives, powerups, enemies, enemy_speeds
    player_x, player_y = WIDTH // 2, HEIGHT // 2
    start_time = time.time()
    moving_walls = [
        pygame.Rect(150, 150, 20, 80),
        pygame.Rect(450, 250, 20, 80)
    ]
    moving_directions = [1, -1]
    moving_speeds = [random.randint(2, 5) for _ in moving_walls]
    walls.append(pygame.Rect(random.randint(50, WIDTH-100), random.randint(50, HEIGHT-20), 100, 20))  # Add a random wall
    goals = [
        pygame.Rect(500, 350, 40, 40),
        pygame.Rect(200, 150, 40, 40),
        pygame.Rect(350, 300, 40, 40)
    ]
    goal_colors = GOAL_COLORS[:len(goals)]
    powerups = [pygame.Rect(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), 20, 20) for _ in range(2)]
    enemies = [
        pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 20, 20),
        pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 20, 20)
    ]
    enemy_speeds = [2, 2]
    level += 1
    player_speed = 5 + level  # Increase speed with level
    lives = 3  # Reset lives

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Pause the game
                pause = not pause
            if event.key == pygame.K_r:  # Restart the level
                reset_game()

    if not pause:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Player boundary handling
        player_x = max(0, min(WIDTH - PLAYER_SIZE, player_x))
        player_y = max(0, min(HEIGHT - PLAYER_SIZE, player_y))

        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

        # Moving walls logic
        for i, wall in enumerate(moving_walls):
            wall.y += moving_directions[i] * moving_speeds[i]
            if wall.top <= 0 or wall.bottom >= HEIGHT:
                moving_directions[i] *= -1
                moving_speeds[i] = random.randint(2, 5)  # Change speed when direction changes

        # Enemies logic
        for i, enemy in enumerate(enemies):
            if random.choice([True, False]):
                enemy.x += enemy_speeds[i]
            else:
                enemy.y += enemy_speeds[i]
            if enemy.left <= 0 or enemy.right >= WIDTH:
                enemy_speeds[i] *= -1
            if enemy.top <= 0 or enemy.bottom >= HEIGHT:
                enemy_speeds[i] *= -1

        # Collision detection
        collision = False
        for wall in walls + moving_walls:
            if player_rect.colliderect(wall):
                collision = True
                break

        for enemy in enemies:
            if player_rect.colliderect(enemy):
                collision = True
                break

        if collision:
            lives -= 1
            if lives <= 0:
                screen.fill(BG_COLOR)
                draw_text("Game Over! Press R to Restart", font, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 2)
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            reset_game()
                            break
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        break

        # Check if the player reaches any goal
        goal_reached = False
        for i, goal in enumerate(goals):
            if player_rect.colliderect(goal):
                goal_reached = True
                score += 100
                goals.remove(goal)
                goal_colors.pop(i)
                if not goals:
                    screen.fill(BG_COLOR)
                    draw_text(f"You Win! Score: {score} | Level: {level}", font, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    reset_game()
                break

        # Check if the player collects any power-up
        for powerup in powerups[:]:
            if player_rect.colliderect(powerup):
                powerups.remove(powerup)
                powerup_timer = time.time() + powerup_duration
                player_speed += 2  # Increase player speed temporarily

        if powerup_timer and time.time() > powerup_timer:
            player_speed = 5 + level  # Reset speed after power-up duration

        screen.fill(BG_COLOR)

        # Draw walls
        for wall in walls + moving_walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)

        # Draw player, goals, power-ups, and enemies
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        for i, goal in enumerate(goals):
            pygame.draw.rect(screen, goal_colors[i], goal)
        for powerup in powerups:
            pygame.draw.rect(screen, POWERUP_COLOR, powerup)
        for enemy in enemies:
            pygame.draw.rect(screen, ENEMY_COLOR, enemy)

        # Timer, score, level, and lives
        elapsed_time = time.time() - start_time
        draw_text(f"Time: {int(elapsed_time)}s | Score: {score} | Level: {level} | Lives: {lives}", font, TEXT_COLOR, screen, WIDTH // 2, 20)

        pygame.display.flip()
        clock.tick(FPS)
