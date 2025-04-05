import pygame
import random
import math
from settings import *
from assets import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        """ Initialize the enemy with its type and properties. """
        super().__init__()
        self.enemy_type = enemy_type  # Type of enemy 
        self.original_image = enemy_img  # Keep original image for rotation
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        
        self.spawn_outside_screen()
        self.pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        
        # Attack-related properties
        self.is_attacking = False
        self.can_attack = True  # Can attack when not in cooldown
        self.attack_frame_index = 0
        self.attack_frame_duration = 150  # Duration per frame
        self.attack_animation_timer = 0  # Timer for animation frames
        self.attack_images = enemy_img_attack  # Attack frames (sprites)
        self.attack_cooldown = ENEMY_ATTACK_CD  # Time between attacks in milliseconds
        self.attack_time = 0  # Time when the enemy can next attack

        # Spawn outside screen
        self.spawn_outside_screen()

        self.health = enemy_type['health']  # Health of the enemy
        self.angle = 0

    def attack_timer(self):
        """ Handles the cooldown for the enemy's attacks. """
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def attack_frames(self):
        """ Start attack animation frames. """
        self.is_attacking = True
        self.attack_frame_index = 0
        self.attack_animation_timer = pygame.time.get_ticks()

    def spawn_outside_screen(self):
        """ Spawns enemy randomly outside the screen edges. """
        spawn_side = random.choice(["top", "bottom", "left", "right"])

        if spawn_side == "top":
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = -self.rect.height
        elif spawn_side == "bottom":
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = HEIGHT + self.rect.height
        elif spawn_side == "left":
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, HEIGHT)
        elif spawn_side == "right":
            self.rect.x = WIDTH + self.rect.width
            self.rect.y = random.randint(0, HEIGHT)

    def rotate_towards_player(self, player):
        """ Rotates the enemy to face the player. """
        player_x, player_y = player.rect.centerx, player.rect.centery
        rel_x, rel_y = player_x - self.rect.centerx, player_y - self.rect.centery
        self.angle = math.degrees(math.atan2(rel_y, rel_x))

        # Rotate from the original image to avoid distortion
        prev_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=prev_center)


    def update(self, player):
        """ Moves enemy toward the player. """
        dx = player.rect.centerx - self.pos.x
        dy = player.rect.centery - self.pos.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            direction = pygame.math.Vector2(dx, dy).normalize()
            self.pos += direction * self.enemy_type['speed']
            self.rect.center = self.pos  # Casts to int under the hood


        self.handle_animation()
        self.rotate_towards_player(player)

    def handle_animation(self):
        current_time = pygame.time.get_ticks()

        if self.is_attacking:
            if current_time - self.attack_animation_timer >= self.attack_frame_duration:
                self.attack_animation_timer = current_time
                self.attack_frame_index += 1
                if self.attack_frame_index >= len(self.attack_images):
                    self.is_attacking = False
                    self.original_image = enemy_img
                else:
                    self.original_image = self.attack_images[self.attack_frame_index]
                
                self.mask = pygame.mask.from_surface(self.original_image)
