# main.py
import random, pygame, math, asyncio
from settings import *
from assets import background_img
from player import Player
from bullet import Bullet
from enemy import Enemy
from utils import *

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

blood_imgs = [load_image(f"./img/blood/blood_hit_0{i}.png") for i in range(1, 4)]
blood_splatters = []  # Stores (image, position)


def draw_health_bar():
    """ Draws the player's health bar on the screen. """
    health_percentage = player.health / PLAYER_HEALTH
    health_bar_width = 200 * health_percentage
    health_bar_height = 20
    health_bar_x = 10
    health_bar_y = 10

    # Draw the background of the health bar
    pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, 200, health_bar_height))

    # Draw the current health
    pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

def draw_ui(killed_enemies):
    """ Draws the UI elements like ammo count and health. """
    if player.ammo_count > 0:
        draw_text(screen, f"Ammo: {player.ammo_count}", (10, 35), 30, BLACK)
    else:
        draw_text(screen, f"Ammo: {player.ammo_count}", (10, 35), 30, BLACK)
        draw_text(screen, "Out of Ammo (R) to reload", (350, 350), 30, RED)
    draw_text(screen, f"Killed: {killed_enemies}", (10, 60), 30, BLACK)
    draw_health_bar()

async def main():
    frame_count = 0
    killed_enemies = 0
    while True:
        screen.blit(background_img, (0, 0))  # Draw background
        keys = pygame.key.get_pressed()

        # Event handling
        player.gun_timer()  # Check if player can shoot
        player.be_hit_timer()  # Check if player can be hit

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Shooting bullets

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not player.is_reloading and player.ammo_count < player.weapon['ammo_capacity']:
                    player.reload_frames()

            
            if event.type == pygame.MOUSEBUTTONDOWN and player.can_shoot and player.ammo_count > 0 and not player.is_reloading:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.degrees(math.atan2(mouse_y - player.rect.centery, mouse_x - player.rect.centerx))
                player.shoot_frames()
                bullet_group.add(Bullet(player.rect.centerx, player.rect.centery, angle, player.weapon['bullet_speed']))
                player.ammo_count -= 1
                player.can_shoot = False
                player.shoot_time = pygame.time.get_ticks()

        # Spawn enemies over time
        if frame_count % ENEMY_SPAWN_RATE == 0 and len(enemy_group) < NUM_ENEMIES:  # Limit to 5 enemies
            enemy_group.add(Enemy(ENEMY_TYPES['zombie']))

        # Update objects
        player_group.update(keys)
        bullet_group.update()
        enemy_group.update(player)

        # Collision detection (Bullets hitting enemies)
        for bullet in bullet_group:
            hit_enemy = pygame.sprite.spritecollideany(bullet, enemy_group)
            if hit_enemy:
                hit_enemy.health -= player.weapon['damage']
                bullet.kill()
                if hit_enemy.health <= 0:
                    hit_enemy.kill()
                    killed_enemies += 1
                    blood_splatters.append((random.choice(blood_imgs), hit_enemy.rect.center))

        # Check for collision between player and enemies
        # Collision detection when enemy is attacking
        for enemy in enemy_group:
            enemy.attack_timer()  # Check cooldown
            if pygame.sprite.collide_mask(player, enemy) and enemy.can_attack:
                # Player gets hit during the attack animation
                if player.can_be_hit:
                    player.can_be_hit = False  # Prevent multiple hits in quick succession
                    enemy.attack_frames()  # Trigger attack animation
                    enemy.can_attack = False  # Prevent immediate consecutive attacks
                    player.health -= enemy.enemy_type['damage']
                    player.hit_time = pygame.time.get_ticks()  # Set the time when player was hit
                    blood_splatters.append((random.choice(blood_imgs), player.rect.center))

        # Draw everything
        # Draw blood splatters first so they appear under everything
        for img, pos in blood_splatters:
            screen.blit(img, pos)
        player_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)

        draw_ui(killed_enemies)

        pygame.display.flip()
        clock.tick(FPS)
        frame_count += 1
        await asyncio.sleep(0)
    
asyncio.run(main())
