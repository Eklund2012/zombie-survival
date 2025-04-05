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
        'damage': 1,
        'range': 300,
        'cooldown': 1000,  # milliseconds
        'bullet_speed': 10,
        'ammo_capacity': 10,
    },
    'rifle': {
        'damage': 15,
        'cooldown': 300,  # milliseconds
        'bullet_speed': 15,
        'ammo_capacity': 30,
    },
    'shotgun': {
        'damage': 20,
        'range': 200,
        'cooldown': 200,  # milliseconds
        'bullet_speed': 8,
        'ammo_capacity': 8,
    },
}

# Animation settings
SHOOT_FRAME_DUR = 50

# Bullet settings
BULLET_SIZE = (12, 7)    

# Enemy settings
ENEMY_SIZE = (80, 80)
ENEMY_SIZE_ATTACK = (80 + 20, 80 + 20)
NUM_ENEMIES = 5
ENEMY_ATTACK_CD = 1000
ENEMY_SPEED = 1
ENEMY_SPAWN_RATE = 50  # Lower = more enemies

ENEMY_TYPES = {
    'zombie': {
        'health': 3,
        'damage': 1,
        'speed': 1,
    },
}