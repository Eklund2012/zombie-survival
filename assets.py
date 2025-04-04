# assets.py
import pygame
from settings import *
from utils import *

# Ensure pygame is initialized before loading assets
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Temporary screen setup

# Load images
player_img = load_image("./img/Top_Down_Survivor/rifle/idle/survivor-idle_rifle_0.png", PLAYER_SIZE)

enemy_img = pygame.Surface((30, 30))
enemy_img.fill((255, 0, 0))  # Red color

bullet_img = load_image("./img/bullet.png", BULLET_SIZE)

background_img = load_image("./img/background-1.png", (WIDTH, HEIGHT))

pygame.display.quit()
