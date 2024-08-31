import pygame

# Ustawienia ekranu
pygame.init()
display_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

# Tytuł
game_title = "Endless Wave Runner"
pygame.display.set_caption(game_title)

# Ikona gry
icon_url = "https://firebasestorage.googleapis.com/v0/b/endless-wave-runner.appspot.com/o/icon.webp?alt=media&token=86abe24a-9369-4ac9-8435-a99a76344f59"
programIcon = None

# Czcionka
font_url = "https://firebasestorage.googleapis.com/v0/b/endless-wave-runner.appspot.com/o/8514fixe.ttf?alt=media&token=6df9d68d-0299-47da-bc4f-ad2cd5f7131e"
font = None

# Skalowanie elementów gry
w_scale = SCREEN_WIDTH / 1920
h_scale = SCREEN_HEIGHT / 1080

# PNG myszki w How to play
mouse_png_url = "https://firebasestorage.googleapis.com/v0/b/endless-wave-runner.appspot.com/o/mouse.png?alt=media&token=46763929-632f-442b-a16b-4b63ef17e1b5"

# Ustawienia mapy
MAP_WIDTH, MAP_HEIGHT = 3000, 2000

# Kolory
WHITE = (255, 255, 255)
LIGHT_GREY = (140, 140, 140)
GREY = (100, 100, 100)
LITTLE_DARK_GREY = (80, 80, 80)
DARK_GREY = (60, 60, 60)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 150)
YELLOW = (255, 255, 0)

# Ustawienia gracza
player_speed = 5
player_damage = 10
player_max_health = 100

player_speed_limit = 12
player_damage_limit = 50
player_max_health_limit = 300

weapon_length = 30
weapon_width = 5

player_blinking_time = 2000

# Ustawienia przeciwników
enemy_health = 20
enemy_speed = 3
boss_health_multiplier = 3
boss_speed = 2
enemy_speed_change = 0
enemy_damage = 20
knockback = 25

x_waves_to_encrease_enemy_health = 5
enemy_health_encrease_value = 10
x_waves_to_encrease_enemy_speed = 20
enemy_speed_encrease_value = 1
x_waves_to_boss_wave = 5
max_enemies_spawn = 20

boss_message_duration = 3000
more_speed_message_duration = 3000

# Ustawienia strzelania
shot_interval = 0.2
bullet_speed = 15

# Ustawienia przedmiotów
time_to_pickup = 30000
blinking_time = 5000

boost_chance = 0.4
speed_chance = 0.1
drop_from_normal_enemy_chance = 0.05

healing_value = 20
health_boost_value = 50
damage_boost_value = 5
speed_boost_value = 1

# Pozostałe
max_fps = 90
