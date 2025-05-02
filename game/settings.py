# settings.py

# Game settings
WIDTH, HEIGHT = 900, 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Player settings
PLAYER_SPEED = 4
PLAYER_SIZE = (80, 80)
PLAYER_SIZE_RELOAD = (80 + 3, 80 + 3)
PLAYER_HEALTH = 100
PLAYER_HIT_TIME = 1000  # milliseconds

WEAPON_TYPES = {
    'handgun': {
        'name': 'Handgun',
        'damage': 1,
        'cooldown': 800,  # milliseconds
        'bullet_speed': 10,
        'ammo_capacity': 10,
    },
    'rifle': {
        'name': 'Rifle',
        'damage': 3,
        'cooldown': 200,  # milliseconds
        'bullet_speed': 15,
        'ammo_capacity': 30,
    },
    'shotgun': {
        'name': 'Shotgun',
        'damage': 6,
        'cooldown': 200,  # milliseconds
        'bullet_speed': 8,
        'ammo_capacity': 8,
    },
}

# Animation settings
SHOOT_FRAME_DUR = 50
RELOAD_FRAME_DUR = 100

# Bullet settings
BULLET_SIZE = (12, 7)    

# Enemy settings
ENEMY_SIZE = (80, 80)
ENEMY_SIZE_ATTACK = (80 + 22, 80 + 22)
ENEMY_ATTACK_CD = 1000
ENEMY_SPEED = 1

ENEMY_TYPES = {
    'zombie': {
        'img': "img/export/skeleton-idle_2.png",
        'size': (80, 80),
        'health': 3,
        'damage': 5,
        'speed': 1,
        'attack_speed': 1000,
    },
}

# Wave settings
WAVE_TYPES = {
    'easy': {
        'enemy_count': 1, # amount of enemies on the screen
        'enemies_per_wave': 1, # amount of enemies spawned per wave
        'enemy_type': {
                        'zombie'
                      },  
        'spawn_rate': 50,
    },
    'medium': {
        'enemy_count': 2,
        'enemies_per_wave': 2,
        'enemy_type': {
                        'zombie',
                      },
        'spawn_rate': 40,
    },
    'hard': {
        'enemy_count': 3,
        'enemies_per_wave': 3,
        'enemy_type': 'zombie',
        'spawn_rate': 30,
    },
    'ffa': {
        'enemy_count': 10000,
        'enemies_per_wave': 10000,
        'enemy_type': 'zombie',
        'spawn_rate': 30,
    },
}

# Bomb settings
BOMB_SIZE = (50, 50)
EXPLOSION_SIZE = (100, 100)
BOMB_SPEED = 5

# Mouse settings
LEFT = 1
MIDDLE = 2
RIGHT = 3

# Crosshair settings
CROSSHAIR_SIZE = (50, 50)