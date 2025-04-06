import pygame, random, math, asyncio
from .settings import *
from .assets import background_img
from .player import Player
from .bullet import Bullet
from .enemy import Enemy
from .utils import draw_text, load_image

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Top-Down Shooter Survival")
        self.clock = pygame.time.Clock()

        # Player & groups
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.blood_imgs = [load_image(f"./img/blood/blood_hit_0{i}.png") for i in range(1, 4)]
        self.blood_splatters = []

        self.killed_enemies = 0
        self.frame_count = 0

    def draw_health_bar(self):
        health_percentage = self.player.health / PLAYER_HEALTH
        health_bar_width = 200 * health_percentage
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, 200, 20))
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, health_bar_width, 20))

    def draw_ui(self):
        if self.player.ammo_count > 0:
            draw_text(self.screen, f"Ammo: {self.player.ammo_count}", (10, 35), 30, BLACK)
        else:
            draw_text(self.screen, f"Ammo: {self.player.ammo_count}", (10, 35), 30, BLACK)
            draw_text(self.screen, "Out of Ammo (R) to reload", (350, 350), 30, RED)
        draw_text(self.screen, f"Killed: {self.killed_enemies}", (10, 60), 30, BLACK)
        self.draw_health_bar()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not self.player.is_reloading and self.player.ammo_count < self.player.weapon['ammo_capacity']:
                    self.player.reload_frames()

            if event.type == pygame.MOUSEBUTTONDOWN and self.player.can_shoot and self.player.ammo_count > 0 and not self.player.is_reloading:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.degrees(math.atan2(mouse_y - self.player.rect.centery, mouse_x - self.player.rect.centerx))
                self.player.shoot_frames()
                self.bullet_group.add(Bullet(self.player.rect.centerx, self.player.rect.centery, angle, self.player.weapon['bullet_speed']))
                self.player.ammo_count -= 1
                self.player.can_shoot = False
                self.player.shoot_time = pygame.time.get_ticks()

    def update(self, keys):
        self.player.gun_timer()
        self.player.be_hit_timer()

        if self.frame_count % ENEMY_SPAWN_RATE == 0 and len(self.enemy_group) < NUM_ENEMIES:
            self.enemy_group.add(Enemy(ENEMY_TYPES['zombie']))

        self.player_group.update(keys)
        self.bullet_group.update()
        self.enemy_group.update(self.player)

        for bullet in self.bullet_group:
            hit_enemy = pygame.sprite.spritecollideany(bullet, self.enemy_group)
            if hit_enemy:
                hit_enemy.health -= self.player.weapon['damage']
                bullet.kill()
                if hit_enemy.health <= 0:
                    hit_enemy.kill()
                    self.killed_enemies += 1
                    self.blood_splatters.append((random.choice(self.blood_imgs), hit_enemy.rect.center))

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

        for img, pos in self.blood_splatters:
            self.screen.blit(img, pos)

        self.player_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.enemy_group.draw(self.screen)

        self.draw_ui()
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
