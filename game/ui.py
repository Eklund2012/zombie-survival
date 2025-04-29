# ui.py
import pygame
from .settings import PLAYER_HEALTH, BLACK, RED
from .utils import draw_text
from .assets import bomb_img, crosshair_img

def draw_health_bar(screen, player):
    health_percentage = player.health / PLAYER_HEALTH
    health_bar_width = 200 * health_percentage
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, health_bar_width, 20))

def draw_ui(screen, player, killed_enemies, blood_splatters):
    # Ammo text
    draw_text(screen, f"Ammo: {player.ammo_count}", (10, 35), 30, BLACK)
    if player.ammo_count == 0:
        draw_text(screen, "Out of Ammo (R) to reload", (350, 350), 30, RED)

    draw_text(screen, f"Zombies Killed: {killed_enemies}", (10, 60), 30, BLACK)
    draw_health_bar(screen, player)
    draw_bombs(screen, player.bombs)
    draw_blood_splatters(screen, blood_splatters)
    draw_crosshair(screen)

def draw_crosshair(screen):
    mouse_pos = pygame.mouse.get_pos()
    crosshair_rect = crosshair_img.get_rect(center=mouse_pos)
    screen.blit(crosshair_img, crosshair_rect)

def draw_blood_splatters(screen, blood_splatters):
    for img, pos in blood_splatters:
        screen.blit(img, pos)

def draw_bombs(screen, bombs):
    it = 0
    while it < bombs:
        pos = (10 + (it * 50), 85)
        screen.blit(bomb_img, pos)
        it += 1   

