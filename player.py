# player.py
import pygame
import math
from settings import *
from assets import player_img

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = player_img  # Store original image for rotation
        self.image = self.original_image  
        self.rect = self.image.get_rect(center=(x, y))
        self.health = PLAYER_HEALTH
        self.angle = 0  # Rotation angle
        self.can_shoot = True  # Shooting cooldown
        self.shoot_time = 0  # Time since last shot
        self.gun_cooldown = PLAYER_GUN_COOLDOWN

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def update(self, keys):
        # Movement logic
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

        # **Rotate Player Toward Mouse**
        self.rotate_towards_mouse()

    def rotate_towards_mouse(self):
        """ Rotates the player to face the mouse cursor. """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Calculate angle between player and mouse
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = math.degrees(math.atan2(rel_y, rel_x))

        # Rotate image and maintain position
        self.image = pygame.transform.rotate(self.original_image, -self.angle)  # Invert because pygame rotates counterclockwise
        self.rect = self.image.get_rect(center=self.rect.center)  # Keep position centered

