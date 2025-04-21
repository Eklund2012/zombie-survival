import pygame
import math
from .bullet import Bullet
from .bomb import Bomb
from .settings import LEFT, RIGHT

class EventHandler:
    def __init__(self, player, bullet_group):
        self.player = player
        self.bullet_group = bullet_group

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousebutton(event)

    def _handle_keydown(self, event):
        if event.key == pygame.K_r:
            if not self.player.is_reloading and self.player.ammo_count < self.player.weapon['ammo_capacity']:
                self.player.reload_frames()

    def _handle_mousebutton(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse_y - self.player.rect.centery, mouse_x - self.player.rect.centerx))

        if event.button == LEFT:
            self._shoot_bullet(angle)
        elif event.button == RIGHT:
            self._throw_bomb(angle)

    def _shoot_bullet(self, angle):
        if self.player.can_shoot and self.player.ammo_count > 0 and not self.player.is_reloading:
            self.player.shoot_frames()
            self.bullet_group.add(Bullet(
                self.player.rect.centerx,
                self.player.rect.centery,
                angle,
                self.player.weapon['bullet_speed']
            ))
            self.player.ammo_count -= 1
            self.player.can_shoot = False
            self.player.shoot_time = pygame.time.get_ticks()

    def _throw_bomb(self, angle):
        if self.player.bombs > 0:
            self.bullet_group.add(Bomb(
                self.player.rect.centerx,
                self.player.rect.centery,
                angle
            ))
            self.player.bombs -= 1
