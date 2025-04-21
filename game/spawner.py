import pygame
from .enemy import Enemy
from .settings import ENEMY_TYPES

class EnemySpawner:
    def __init__(self, enemy_group, wave_state):
        self.enemy_group = enemy_group
        self.wave_state = wave_state
        self.spawned_enemies_per_wave = 0

    def reset_wave(self):
        self.spawned_enemies_per_wave = 0

    def set_wave_state(self, wave_state):
        self.wave_state = wave_state

    def spawn_enemies(self, frame_count):
        if frame_count % self.wave_state['spawn_rate'] == 0:
            if len(self.enemy_group) < self.wave_state['enemy_count']:
                if self.spawned_enemies_per_wave < self.wave_state['enemies_per_wave']:
                    self.enemy_group.add(Enemy(ENEMY_TYPES['zombie']))
                    self.spawned_enemies_per_wave += 1
