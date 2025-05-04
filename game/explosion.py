from .assets import explosion_frames
import pygame

class Explosion:
    def __init__(self, pos, register_kill_callback):
        self.frames = explosion_frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.timer = 0
        self.finished = False
        self.hit_zombies = set()
        self.register_kill = register_kill_callback

    def update(self, zombies):
        self.timer += 1
        if self.timer % 10 == 0:
            self.index += 1
            if self.index >= len(self.frames):
                self.finished = True
            else:
                self.image = self.frames[self.index]
                self.rect = self.image.get_rect(center=self.rect.center)

        # Check for zombies in explosion area
        for zombie in zombies:
            if self.rect.colliderect(zombie.rect) and zombie not in self.hit_zombies:
                self.hit_zombies.add(zombie)
                zombie.kill()
                self.register_kill(zombie, None)


    def draw(self, screen):
        if not self.finished:
            screen.blit(self.image, self.rect)
