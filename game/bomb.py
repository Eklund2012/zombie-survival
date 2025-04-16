# bullet.py
import pygame
import math
from .settings import *
from .assets import bomb_img

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = bomb_img
        self.bullet_speed = BOMB_SPEED
        self.rect = self.image.get_rect(center=(x , y))
        self.dx = math.cos(math.radians(angle)) * self.bullet_speed
        self.dy = math.sin(math.radians(angle)) * self.bullet_speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
