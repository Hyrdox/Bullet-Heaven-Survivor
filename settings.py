import pygame

# Ustawienia ekranu
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Heaven Survivor")

# Ustawienia mapy
MAP_WIDTH, MAP_HEIGHT = 1600, 1200

# Kolory
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
LIGHT_GREY = (80, 80, 80)
DARK_GREY = (60, 60, 60)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Ustawienia gracza
player_speed = 5
player_damage = 10
player_max_health = 100
player_blinking_time = 2000

# Ustawienia przeciwników
enemy_health = 20
enemy_speed = 3
boss_health_multiplier = 3  # multiplied by current enemy health
boss_speed = 2
enemy_speed_change = 0
enemy_damage = 20
knockback = 10
boss_message_duration = 3000

# Ustawienia strzelania
shot_interval = 0.2
bullet_speed = 10

# Ustawienia przedmiotów
time_to_pickup = 30000
blinking_time = 5000

potion_chance = 0.6
boost_chance = 0.15
no_drop_chance = 0.1
