# player.py
import pygame
import math
from .settings import *
from .assets import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = player_img_handgun_idle
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.health = PLAYER_HEALTH
        self.angle = 0
        self.can_shoot = True
        self.weapon = WEAPON_TYPES['handgun']         
        self.gun_cooldown = self.weapon['cooldown']
        self.ammo_count = self.weapon['ammo_capacity']
        self.shoot_time = 0  # Time when the player can next shoot

        # Animation-related
        self.is_shooting = False
        self.shoot_frame_index = 0
        self.shoot_animation_timer = 0
        self.shoot_handgun_images = player_img_handgun_shoot
        self.shoot_frame_duration = SHOOT_FRAME_DUR  # milliseconds between frames

        self.is_reloading = False
        self.reload_frame_index = 0
        self.reload_animation_timer = 0
        self.reload_handgun_images = player_img_handgun_reload
        self.reload_frame_duration = RELOAD_FRAME_DUR  # Adjust this to your liking

        self.can_be_hit = True  # Player can be hit by enemies
        self.hit_time = 0


    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def be_hit_timer(self):
        """ Timer to control the invincibility frame after being hit. """
        if not self.can_be_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= PLAYER_HIT_TIME:  # PLAYER_HIT_TIME is the cooldown time for being hit
                self.can_be_hit = True

    def reload_frames(self):
        self.is_reloading = True
        self.reload_frame_index = 0
        self.reload_animation_timer = pygame.time.get_ticks()
        self.can_shoot = False  # Prevent shooting during reload


    def shoot_frames(self):
        self.is_shooting = True
        self.shoot_frame_index = 0
        self.shoot_animation_timer = pygame.time.get_ticks()

    def update(self, keys):
        # Movement
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

        # Handle animation
        self.handle_animation()

        # Rotate
        self.rotate_towards_mouse()

    def handle_animation(self):
        current_time = pygame.time.get_ticks()

        if self.is_reloading:
            if current_time - self.reload_animation_timer >= self.reload_frame_duration:
                self.reload_animation_timer = current_time
                if self.reload_frame_index < len(self.reload_handgun_images):
                    self.original_image = self.reload_handgun_images[self.reload_frame_index]
                    self.mask = pygame.mask.from_surface(self.original_image)  # Update mask for new image
                    self.reload_frame_index += 1
                else:
                    self.is_reloading = False
                    self.original_image = player_img_handgun_idle
                    self.ammo_count = self.weapon['ammo_capacity']
                    self.can_shoot = True

        elif self.is_shooting:
            if current_time - self.shoot_animation_timer >= self.shoot_frame_duration:
                self.shoot_animation_timer = current_time
                self.shoot_frame_index += 1
                if self.shoot_frame_index >= len(self.shoot_handgun_images):
                    self.is_shooting = False
                    self.original_image = player_img_handgun_idle
                else:
                    self.original_image = self.shoot_handgun_images[self.shoot_frame_index]



    def rotate_towards_mouse(self):
        """ Rotates the player to face the mouse cursor. """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Calculate angle between player and mouse
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = math.degrees(math.atan2(rel_y, rel_x))

        # Rotate image and maintain position
        self.image = pygame.transform.rotate(self.original_image, -self.angle)  # Invert because pygame rotates counterclockwise
        self.rect = self.image.get_rect(center=self.rect.center)  # Keep position centered

