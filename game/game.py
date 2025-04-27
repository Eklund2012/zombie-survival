import pygame, random, asyncio, os
from .settings import *
from .assets import *
from .player import Player
from .bomb import Bomb
from .bullet import Bullet
from .events import EventHandler
from .spawner import EnemySpawner
from .utils import load_image
from .ui import draw_ui, draw_blood_splatters

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.mouse.set_visible(False) # Hide cursor here
        
        self.clock = pygame.time.Clock()
        self.wave_state = WAVE_TYPES['easy']  # Default wave state

        # Player & groups
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.blood_imgs = [load_image(f"./img/blood/blood_hit_0{i}.png") for i in range(1, len(os.listdir("./img/blood")) + 1)]
        self.blood_splatters = []

        self.killed_enemies = 0
        self.killed_enemies_per_wave = 0
        self.frame_count = 0

        self.event_handler = EventHandler(self.player, self.bullet_group)
        self.spawner = EnemySpawner(self.enemy_group, self.wave_state)

    def update(self, keys):
        self.player.gun_timer()
        self.player.be_hit_timer()

        self.spawner.spawn_enemies(self.frame_count)

        self.player_group.update(keys)
        self.bullet_group.update()
        self.enemy_group.update(self.player, self.enemy_group)

        self.handle_bullet_enemy_collisions()

    def handle_bullet_enemy_collisions(self):
        for bullet in self.bullet_group:
            hit_enemy = pygame.sprite.spritecollideany(bullet, self.enemy_group)
            if hit_enemy:
                bullet.kill()
                damage = self.player.weapon['damage'] if isinstance(bullet, Bullet) else hit_enemy.health
                hit_enemy.health -= damage
                if hit_enemy.health <= 0:
                    self.register_enemy_kill(hit_enemy)

    def register_enemy_kill(self, enemy):
        enemy.kill()
        self.blood_splatters.append((random.choice(self.blood_imgs), enemy.rect.center))
        self.killed_enemies += 1
        self.killed_enemies_per_wave += 1
        if self.killed_enemies_per_wave >= self.wave_state['enemies_per_wave']:
            self.change_wave(self.wave_state)

    def change_wave(self, current_wave):
        if current_wave == WAVE_TYPES['easy']:
            print("Wave 1 completed!")
            self.wave_state = WAVE_TYPES['medium']         
            self.player.weapon = WEAPON_TYPES['rifle']            
            self.player.original_image = player_img_rifle_idle
            self.player.shoot_images = player_img_rifle_shoot
            self.player.reload_images = player_img_rifle_reload
        elif current_wave == WAVE_TYPES['medium']:
            print("Wave 2 completed!")
            self.wave_state = WAVE_TYPES['hard']
            self.player.weapon = WEAPON_TYPES['shotgun']
            self.player.original_image = player_img_shotgun_idle
            self.player.shoot_images = player_img_shotgun_shoot
            self.player.reload_images = player_img_shotgun_reload
        elif current_wave == WAVE_TYPES['hard']:
            print("You have completed the game!")
            self.spawner.disable_spawning()
        self.killed_enemies_per_wave = 0
        self.player.ammo_count = self.player.weapon['ammo_capacity']
        self.spawner.set_wave_state(self.wave_state)
        self.spawner.reset_wave()

    def draw(self):
        self.screen.blit(background_img, (0, 0))

        self.player_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.enemy_group.draw(self.screen)

        draw_ui(self.screen, self.player, self.killed_enemies, self.blood_splatters)
        pygame.display.flip()

    async def run(self):
        while True:
            keys = pygame.key.get_pressed()
            self.event_handler.handle_events()
            self.update(keys)
            self.draw()

            pygame.display.set_caption("Top-Down Shooter Survival - FPS: {:.2f}".format(self.clock.get_fps()))

            self.clock.tick(FPS)
            self.frame_count += 1
            await asyncio.sleep(0)
