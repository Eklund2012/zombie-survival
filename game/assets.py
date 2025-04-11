# assets.py
import pygame
from .settings import *
from .utils import *

# Ensure pygame is initialized before loading assets
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Temporary screen setup

# Load images 
player_img_handgun_idle = load_image("img/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_0.png", PLAYER_SIZE)
player_img_handgun_shoot = load_image_sequence("img/Top_Down_Survivor/handgun/shoot/survivor-shoot_handgun_{}.png",
                                               3,
                                               PLAYER_SIZE)
player_img_handgun_reload = load_image_sequence(
    "img/Top_Down_Survivor/handgun/reload/survivor-reload_handgun_{}.png", 
    15, 
    PLAYER_SIZE_RELOAD
)

player_img_rifle_idle = load_image("img/Top_Down_Survivor/rifle/idle/survivor-idle_rifle_0.png", PLAYER_SIZE)
player_img_rifle_shoot = load_image_sequence("img/Top_Down_Survivor/rifle/shoot/survivor-shoot_rifle_{}.png",
                                               3,
                                                PLAYER_SIZE)
player_img_rifle_reload = load_image_sequence(
    "img/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_{}.png", 
    15, 
    PLAYER_SIZE_RELOAD
)

enemy_img_attack_zombie = load_image_sequence("img/export/skeleton-attack_{}.png", 9, ENEMY_SIZE_ATTACK)

bullet_img = load_image("img/bullet.png", BULLET_SIZE)

background_img = load_image("img/background-1.png", (WIDTH, HEIGHT))

pygame.display.quit()