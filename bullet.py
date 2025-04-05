# bullet.py
import pygame
import math
from settings import *
from assets import bullet_img

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, bullet_speed):
        super().__init__()
        self.image = bullet_img
        self.bullet_speed = bullet_speed
        self.rect = self.image.get_rect(center=(x , y))
        self.dx = math.cos(math.radians(angle)) * self.bullet_speed
        self.dy = math.sin(math.radians(angle)) * self.bullet_speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
