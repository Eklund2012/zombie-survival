# bullet.py
import pygame
import math
from settings import BULLET_SPEED, WIDTH, HEIGHT
from assets import bullet_img

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x , y))
        self.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.dy = math.sin(math.radians(angle)) * BULLET_SPEED

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
