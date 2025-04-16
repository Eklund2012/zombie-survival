import pygame, random, math, asyncio
from .settings import *
from .assets import *
from .player import Player
from .bomb import Bomb
from .bullet import Bullet
from .enemy import Enemy
from .utils import load_image
from .ui import draw_ui, draw_blood_splatters

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Top-Down Shooter Survival")
        self.clock = pygame.time.Clock()
        self.wave_state = WAVE_TYPES['easy']  # Default wave state

        # Player & groups
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.blood_imgs = [load_image(f"./img/blood/blood_hit_0{i}.png") for i in range(1, 4)]
        self.blood_splatters = []

        self.killed_enemies = 0
        self.killed_enemies_per_wave = 0
        self.spawned_enemies_per_wave = 0
        self.frame_count = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not self.player.is_reloading and self.player.ammo_count < self.player.weapon['ammo_capacity']:
                    self.player.reload_frames()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT and self.player.can_shoot and self.player.ammo_count > 0 and not self.player.is_reloading:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    angle = math.degrees(math.atan2(mouse_y - self.player.rect.centery, mouse_x - self.player.rect.centerx))
                    self.player.shoot_frames()
                    self.bullet_group.add(Bullet(self.player.rect.centerx, self.player.rect.centery, angle, self.player.weapon['bullet_speed']))
                    self.player.ammo_count -= 1
                    self.player.can_shoot = False
                    self.player.shoot_time = pygame.time.get_ticks()
                elif event.button == RIGHT and self.player.bombs > 0:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    angle = math.degrees(math.atan2(mouse_y - self.player.rect.centery, mouse_x - self.player.rect.centerx))
                    self.bullet_group.add(Bomb(self.player.rect.centerx, self.player.rect.centery, angle))
                    self.player.bombs -= 1
                    # Bomb explosion logic here (not implemented in this snippet)

    def update(self, keys):
        self.player.gun_timer()
        self.player.be_hit_timer()

        if self.frame_count % self.wave_state['spawn_rate'] == 0: # Spawn rate of enemies
            if len(self.enemy_group) < self.wave_state['enemy_count']: # Max enemies on screen
                if self.spawned_enemies_per_wave < self.wave_state['enemies_per_wave']: # Spawned enemies per wave
                    self.enemy_group.add(Enemy(ENEMY_TYPES['zombie']))
                    self.spawned_enemies_per_wave += 1

        self.player_group.update(keys)
        self.bullet_group.update()
        self.enemy_group.update(self.player, self.enemy_group)

        for bullet in self.bullet_group:
            hit_enemy = pygame.sprite.spritecollideany(bullet, self.enemy_group)
            if hit_enemy and isinstance(bullet, Bullet):
                hit_enemy.health -= self.player.weapon['damage']
                bullet.kill()
                if hit_enemy.health <= 0:
                    hit_enemy.kill()
                    self.killed_enemies += 1
                    self.killed_enemies_per_wave += 1
                    if self.killed_enemies_per_wave >= self.wave_state['enemies_per_wave'] and self.wave_state == WAVE_TYPES['easy']:
                        print("medium wave")
                        self.wave_state = WAVE_TYPES['medium']
                        self.player.weapon = WEAPON_TYPES['rifle']
                        self.player.ammo_count = self.player.weapon['ammo_capacity']
                        self.player.original_image = player_img_rifle_idle
                        self.player.shoot_images = player_img_rifle_shoot
                        self.player.reload_images = player_img_rifle_reload
                        self.killed_enemies_per_wave = 0
                        self.spawned_enemies_per_wave = 0
                    elif self.killed_enemies_per_wave >= self.wave_state['enemies_per_wave'] and self.wave_state == WAVE_TYPES['medium']:
                        print("hard wave")
                        self.wave_state = WAVE_TYPES['hard']
                        self.killed_enemies_per_wave = 0
                        self.spawned_enemies_per_wave = 0
                    self.blood_splatters.append((random.choice(self.blood_imgs), hit_enemy.rect.center))
            elif hit_enemy and isinstance(bullet, Bomb):
                #self.screen.blit(explosion_img, hit_enemy.rect.center)
                hit_enemy.kill()
                bullet.kill()
                

        for enemy in self.enemy_group:
            enemy.attack_timer()
            if pygame.sprite.collide_mask(self.player, enemy) and enemy.can_attack:
                if self.player.can_be_hit:
                    self.player.can_be_hit = False
                    enemy.attack_frames()
                    enemy.can_attack = False
                    self.player.health -= enemy.enemy_type['damage']
                    self.player.hit_time = pygame.time.get_ticks()
                    self.blood_splatters.append((random.choice(self.blood_imgs), self.player.rect.center))

    def draw(self):
        self.screen.blit(background_img, (0, 0))
        draw_blood_splatters(self.screen, self.blood_splatters)

        self.player_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.enemy_group.draw(self.screen)

        draw_ui(self.screen, self.player, self.killed_enemies)
        pygame.display.flip()

    async def run(self):
        while True:
            keys = pygame.key.get_pressed()
            self.handle_events()
            self.update(keys)
            self.draw()

            self.clock.tick(FPS)
            self.frame_count += 1
            await asyncio.sleep(0)
