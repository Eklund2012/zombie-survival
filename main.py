# main.py
import pygame
import math
from settings import WIDTH, HEIGHT, FPS, ENEMY_SPAWN_RATE
from assets import background_img
from player import Player
from bullet import Bullet
from enemy import Enemy

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter Survival")

# Game Clock
clock = pygame.time.Clock()

# Groups
player = Player(WIDTH // 2, HEIGHT // 2)
player_group = pygame.sprite.GroupSingle(player)
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

running = True
frame_count = 0

while running:
    screen.blit(background_img, (0, 0))  # Draw background
    keys = pygame.key.get_pressed()

    # Event handling
    player.gun_timer()  # Check if player can shoot
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shooting bullets
        if event.type == pygame.MOUSEBUTTONDOWN and player.can_shoot:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.degrees(math.atan2(mouse_y - player.rect.centery, mouse_x - player.rect.centerx))
            bullet_group.add(Bullet(player.rect.centerx, player.rect.centery, angle))
            player.can_shoot = False
            player.shoot_time = pygame.time.get_ticks()

    # Spawn enemies over time
    if frame_count % ENEMY_SPAWN_RATE == 0:
        enemy_group.add(Enemy())

    # Update objects
    player_group.update(keys)
    bullet_group.update()
    enemy_group.update(player)

    # Collision detection (Bullets hitting enemies)
    for bullet in bullet_group:
        hit_enemy = pygame.sprite.spritecollideany(bullet, enemy_group)
        if hit_enemy:
            hit_enemy.health -= 1
            bullet.kill()
            if hit_enemy.health <= 0:
                hit_enemy.kill()

    # Draw everything
    player_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

pygame.quit()
