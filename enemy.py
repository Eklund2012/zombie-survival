# enemy.py
import pygame
import random
import math
from settings import ENEMY_SPEED, WIDTH, HEIGHT
from assets import enemy_img

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()

        # Spawn outside screen
        self.spawn_outside_screen()

        self.health = 3

    def spawn_outside_screen(self):
        """ Spawns enemy randomly outside the screen edges. """
        spawn_side = random.choice(["top", "bottom", "left", "right"])

        if spawn_side == "top":  # Above the screen
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = -self.rect.height
        elif spawn_side == "bottom":  # Below the screen
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = HEIGHT + self.rect.height
        elif spawn_side == "left":  # Left of the screen
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, HEIGHT)
        elif spawn_side == "right":  # Right of the screen
            self.rect.x = WIDTH + self.rect.width
            self.rect.y = random.randint(0, HEIGHT)

    def update(self, player):
        """ Moves enemy toward the player. """
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize direction
            self.rect.x += dx * ENEMY_SPEED
            self.rect.y += dy * ENEMY_SPEED
