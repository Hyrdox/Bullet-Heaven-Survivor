# Importy
import sys
import time
import pygame
import random
import math
import menu
import game_over


# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Heaven Survivor")

# Ustawienia mapy
MAP_WIDTH, MAP_HEIGHT = 1600, 1200

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREY = (60, 60, 60)
LIGHT_GREY = (80, 80, 80)
GREY = (100, 100, 100)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self, damage, health):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK, (25, 25), 26)  # Border
        pygame.draw.circle(self.image, GREEN, (25, 25), 25)
        self.rect = self.image.get_rect()
        self.rect.center = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.speed = 5
        self.health = 100
        self.max_health = health
        self.damage = damage

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < MAP_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < MAP_WIDTH:
            self.rect.x += self.speed

        # Miganie gracza po otrzymaniu obrażeń
        current_time = pygame.time.get_ticks()
        if hasattr(self, 'last_damage_time') and current_time - self.last_damage_time < 2000:  # 2 sekundy migania
            if current_time % 300 < 150:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

# Klasa przeciwnika
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, is_boss=False):
        super().__init__()
        self.image = pygame.Surface((50, 50) if not is_boss else (60, 60), pygame.SRCALPHA)
        self.color = BLACK if is_boss else RED
        pygame.draw.circle(self.image, BLACK, (25, 25) if not is_boss else (30, 30),
                           26 if not is_boss else 31)  # Border
        pygame.draw.circle(self.image, self.color, (25, 25) if not is_boss else (30, 30), 25 if not is_boss else 30)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3 if not is_boss else 2
        self.health = health
        self.max_health = health

    def update(self, player):
        # Przesunięcie w stronę gracza
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            if dist > 50:  # Zachowuje dystans od gracza
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            else:
                self.attack(player, dx, dy)

    def attack(self, player, dx, dy):
        # Zadaj obrażenia i odpychaj gracza
        player.health -= 20
        player.last_damage_time = pygame.time.get_ticks()

        # Odepchnięcie gracza
        knockback_distance = 10
        player.rect.x += dx * knockback_distance
        player.rect.y += dy * knockback_distance

# Klasa pocisku
class Bullet(pygame.sprite.Sprite):
     def __init__(self, x, y, direction, damage):
         super().__init__()
         self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
         pygame.draw.circle(self.image, BLACK, (5, 5), 5)
         self.rect = self.image.get_rect()
         self.rect.center = (x, y)
         self.speed = 10
         self.direction = direction
         self.damage = damage

     def update(self):
         self.rect.x += self.direction[0] * self.speed
         self.rect.y += self.direction[1] * self.speed
         if self.rect.right < 0 or self.rect.left > MAP_WIDTH or self.rect.bottom < 0 or self.rect.top > MAP_HEIGHT:
             self.kill()

# Klasa mikstury
class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, BLACK, [(15, -3), (33, 33), (-3, 33)])  # Border
        pygame.draw.polygon(self.image, GREEN, [(15, 0), (30, 30), (0, 30)])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Sprawdzanie czasu życia mikstury
        elapsed_time = pygame.time.get_ticks() - self.spawn_time

        # Efekt migania w ciągu ostatnich 5 sekund
        if 25000 <= elapsed_time <= 30000:
            if elapsed_time // 250 % 2 == 0:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        elif elapsed_time > 30000:
            self.kill()

# Klasa wzmocnienia obrażeń
class DamageBoost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.image, PURPLE, pygame.Rect(-1, -1, 31, 31))  # Border
        pygame.draw.rect(self.image, PURPLE, pygame.Rect(0, 0, 30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Sprawdzanie czasu życia wzmocnienia
        elapsed_time = pygame.time.get_ticks() - self.spawn_time

        # Efekt migania w ciągu ostatnich 5 sekund
        if 25000 <= elapsed_time <= 30000:
            if elapsed_time // 250 % 2 == 0:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        elif elapsed_time > 30000:
            self.kill()

# Klasa wzmocnienia HP
class HealthBoost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.image, PURPLE, pygame.Rect(-1, -1, 31, 31))  # Border
        pygame.draw.rect(self.image, BLUE, pygame.Rect(0, 0, 30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Sprawdzanie czasu życia wzmocnienia
        elapsed_time = pygame.time.get_ticks() - self.spawn_time

        # Efekt migania w ciągu ostatnich 5 sekund
        if 25000 <= elapsed_time <= 30000:
            if elapsed_time // 250 % 2 == 0:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        elif elapsed_time > 30000:
            self.kill()

# Grupa sprite'ów
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
boosts = pygame.sprite.Group()

# Kamera
camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Generowanie tła
background_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
tile_size = 50
for y in range(0, MAP_HEIGHT, tile_size):
    for x in range(0, MAP_WIDTH, tile_size):
        tile_color = random.choice([DARK_GREY, LIGHT_GREY])
        pygame.draw.rect(background_surface, tile_color, pygame.Rect(x, y, tile_size, tile_size))

# Funkcja rysująca tło
def draw_background():
    screen.blit(background_surface, (-camera.x, -camera.y))

# Funkcja rysująca pasek zdrowia przeciwników
def draw_enemy_health_bar(enemy):
    health_bar_width = 40
    health_bar_height = 5
    fill = (enemy.health / enemy.max_health) * health_bar_width
    outline_rect = pygame.Rect(enemy.rect.centerx - health_bar_width // 2 - camera.x,
                                   enemy.rect.top - 15 - camera.y, health_bar_width, health_bar_height)
    fill_rect = pygame.Rect(enemy.rect.centerx - health_bar_width // 2 - camera.x, enemy.rect.top - 15 - camera.y,
                                fill, health_bar_height)
    pygame.draw.rect(screen, RED, fill_rect)
    pygame.draw.rect(screen, BLACK, outline_rect, 1)

# Funkcja generująca falę przeciwników
def generate_wave(wave_number, base_health):
    global boss_message_start_time

    num_enemies = wave_number * 2
    if wave_number % 5 == 0:
        num_enemies += wave_number // 5  # Dodanie BOSSów
    for i in range(num_enemies):
        is_boss = (i >= wave_number * 2)  # Jeśli to boss, to mamy więcej przeciwników niż numer fali
        health = base_health * (3 if is_boss else 1)
        x = random.choice([random.randint(-100, 0), random.randint(MAP_WIDTH, MAP_WIDTH + 100)])
        y = random.choice([random.randint(-100, 0), random.randint(MAP_HEIGHT, MAP_HEIGHT + 100)])
        enemy = Enemy(x, y, health, is_boss)
        all_sprites.add(enemy)
        enemies.add(enemy)

        # Komunikat "BOSS incoming!" na ekranie
        if is_boss:
            boss_message_start_time = pygame.time.get_ticks()

# Wykrywanie kolizji między przeciwnikami
def resolve_enemy_collisions(enemies):
    for enemy in enemies:
        other_enemies = [e for e in enemies if e != enemy]
        for other_enemy in other_enemies:
            if enemy.rect.colliderect(other_enemy.rect):
                dx = enemy.rect.centerx - other_enemy.rect.centerx
                dy = enemy.rect.centery - other_enemy.rect.centery
                dist = math.hypot(dx, dy)
                if dist == 0:
                    dist = 1  # Uniknięcie dzielenia przez zero
                push_x = dx / dist
                push_y = dy / dist
                enemy.rect.x += push_x
                enemy.rect.y += push_y
                other_enemy.rect.x -= push_x
                other_enemy.rect.y -= push_y

# Funkcja rysująca tekst na ekranie
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def pause_game():
    font_button = pygame.font.Font('8514fixe.fon', 50)
    paused = True

    while paused:
        screen.fill(BLACK)  # Możesz dodać przezroczystość zamiast czarnego tła dla efektu zamrożenia
        draw_text('Paused', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text('Enemies are frozen, time is NOT', font_button, GREY, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 40)


        # Definicja przycisków
        button_continue = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 50, 250, 50)
        button_menu = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 20, 250, 50)

        pygame.draw.rect(screen, GREY, button_continue)
        pygame.draw.rect(screen, GREY, button_menu)

        draw_text('Continue', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25)
        draw_text('Menu', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_continue.collidepoint(event.pos):
                    paused = False  # Wracamy do gry
                if button_menu.collidepoint(event.pos):
                    menu.main_menu()  # Powrót do menu głównego
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False  # Wracamy do gry

        pygame.display.flip()

# Zmienna do śledzenia czasu ostatniego strzału
last_shot_time = 0

# Okres czasu między strzałami w sekundach
shot_interval = 0.2

# Zmienne do kontrolowania komunikatu o bossie
boss_message_start_time = None
boss_message_duration = 3000  # Czas trwania komunikatu (w milisekundach)

# Główna pętla gry
def main_game():
    global left_mouse_button_down, last_shot_time, boss_message_start_time
    wave_number = 1
    kills_count = 0
    base_enemy_health = 20
    running = True
    paused = False
    waiting_for_next_wave = True
    wave_start_ticks = pygame.time.get_ticks()
    game_start_time = None
    left_mouse_button_down = False

    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    boosts.empty()

    # Inicjalizacja gracza
    base_player_damage = 10
    base_player_max_health = 100
    player = Player(base_player_damage, base_player_max_health)
    all_sprites.add(player)

    while running:
        current_time = time.time()  # Bieżący czas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_game()  # Pauzujemy grę
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Lewy przycisk myszy został wciśnięty
                left_mouse_button_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Lewy przycisk myszy został zwolniony
                left_mouse_button_down = False
                last_shot_time = 0

        if not paused:
            # Aktualizacja
            keys = pygame.key.get_pressed()
            player.update(keys)
            enemies.update(player)
            bullets.update()
            boosts.update()

            # Rozwiązywanie kolizji między przeciwnikami
            resolve_enemy_collisions(enemies)

            # Sprawdź, czy lewy przycisk myszy jest wciśnięty, aby strzelać
            if left_mouse_button_down and current_time - last_shot_time >= shot_interval:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = mouse_x + camera.x - player.rect.centerx, mouse_y + camera.y - player.rect.centery
                dist = math.hypot(*direction)
                direction = direction[0] / dist, direction[1] / dist
                bullet = Bullet(player.rect.centerx, player.rect.centery, direction, player.damage)
                all_sprites.add(bullet)
                bullets.add(bullet)

                # Zaktualizuj czas ostatniego strzału
                last_shot_time = current_time

            # Sprawdzenie kolizji pocisków z przeciwnikami
            for bullet in bullets:
                hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
                if hit_enemy:
                    hit_enemy.health -= player.damage
                    bullet.kill()
                    if hit_enemy.health <= 0:
                        # Jeśli zabiliśmy bossa, wypada losowy przedmiot
                        if hit_enemy.color == BLACK:
                            boost_type = random.choice(['potion', 'damage', 'health'])
                            if boost_type == 'potion':
                                potion = HealthPotion(hit_enemy.rect.centerx, hit_enemy.rect.centery)
                                all_sprites.add(potion)
                                boosts.add(potion)
                            if boost_type == 'damage':
                                damage_boost = DamageBoost(hit_enemy.rect.centerx, hit_enemy.rect.centery)
                                all_sprites.add(damage_boost)
                                boosts.add(damage_boost)
                            if boost_type == 'health':
                                damage_boost = HealthBoost(hit_enemy.rect.centerx, hit_enemy.rect.centery)
                                all_sprites.add(damage_boost)
                                boosts.add(damage_boost)
                        hit_enemy.kill()
                        kills_count += 1

            # Sprawdzenie kolizji gracza z przedmiotem
            item_collected = pygame.sprite.spritecollideany(player, boosts)
            if item_collected:
                if isinstance(item_collected, HealthPotion):
                    player.health = min(player.max_health, player.health + 20)
                elif isinstance(item_collected, DamageBoost):
                    if player.damage < 50:
                        player.damage += 5
                elif isinstance(item_collected, HealthBoost):
                    if player.max_health < 300:
                        player.max_health += 50
                item_collected.kill()

            # Aktualizacja kamery
            camera.center = player.rect.center
            camera.clamp_ip(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))

            # Rysowanie
            draw_background()
            for entity in all_sprites:
                screen.blit(entity.image, (entity.rect.x - camera.x, entity.rect.y - camera.y))
                if isinstance(entity, Enemy):
                    draw_enemy_health_bar(entity)

            # Pasek obrażeń gracza
            pygame.draw.rect(screen, BLACK, (10, SCREEN_HEIGHT - 60, 50 * 2, 20), 2)
            pygame.draw.rect(screen, PURPLE, (12, SCREEN_HEIGHT - 58, player.damage * 1.96, 16))
            damage_text = pygame.font.Font('8514fixe.fon', 26).render(f"{player.damage} DMG", True, BLACK)
            screen.blit(damage_text, (60 - damage_text.get_width() // 2, SCREEN_HEIGHT - 60))

            # Pasek zdrowia gracza
            pygame.draw.rect(screen, BLACK, (10, SCREEN_HEIGHT - 30, player.max_health * 2, 20), 2)
            pygame.draw.rect(screen, GREEN, (12, SCREEN_HEIGHT - 28, player.health * 1.96, 16))
            health_text = pygame.font.Font('8514fixe.fon', 26).render(f"{player.health}/{player.max_health} HP", True,
                                                                      BLACK)
            screen.blit(health_text, ((player.max_health + 10) - health_text.get_width() // 2, SCREEN_HEIGHT - 30))

            # Wyświetlanie informacji o fali i odliczaniu do następnej
            font = pygame.font.Font('8514fixe.fon', 36)
            wave_text = font.render(((f"Wave {wave_number}") if game_start_time else (f"Game")) + (
                f" starting in {float('{:.1f}'.format((5050 - (pygame.time.get_ticks() - wave_start_ticks)) / 1000))}" if waiting_for_next_wave else ""),
                                    True, WHITE)
            screen.blit(wave_text, (10, 10))

            # Liczba pozostałych przeciwników
            enemies_left_text = font.render((f"Opponents left: {len(enemies)}") if not waiting_for_next_wave else "", True,
                                            WHITE)
            screen.blit(enemies_left_text, (10, 40))  # Pozycja poniżej "Wave X"

            # Wyświetlanie czasu gry i licznika pokonanych przeciwników
            if game_start_time:
                elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000
                time_text = font.render(f"Time: {elapsed_time // 60}:{elapsed_time % 60:02d}", True, WHITE)
                screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 10))

                kills_text = font.render(f'Kills: {kills_count}', True, WHITE)
                screen.blit(kills_text, (SCREEN_WIDTH - kills_text.get_width() - 10, 40))

            # Wyświetlanie komunikatu "BOSS incoming!"
            if boss_message_start_time:
                elapsed_boss_message_time = pygame.time.get_ticks() - boss_message_start_time
                if elapsed_boss_message_time < boss_message_duration:
                    screen.fill(BLACK, (0, 100, SCREEN_WIDTH, 50))  # Czarne tło dla tekstu
                    current_time = pygame.time.get_ticks()
                    if current_time % 1000 < 300:  # Miganie tekstu
                        boss_text = pygame.font.Font(None, 40).render("BOSS INCOMING!", True, RED)
                        screen.blit(boss_text, (SCREEN_WIDTH // 2 - boss_text.get_width() // 2, 110))
                else:
                    boss_message_start_time = None  # Zresetuj komunikat po upływie czasu

            # Sprawdzenie, czy należy rozpocząć nową falę
            if waiting_for_next_wave and pygame.time.get_ticks() - wave_start_ticks >= 5000:
                waiting_for_next_wave = False
                generate_wave(wave_number, base_enemy_health)
                if game_start_time is None:  # Ustawienie czasu rozpoczęcia gry przy pierwszej fali
                    game_start_time = pygame.time.get_ticks()

            # Jeśli fala się skończyła
            if not enemies and not waiting_for_next_wave:
                waiting_for_next_wave = True
                wave_number += 1
                wave_start_ticks = pygame.time.get_ticks()
                if wave_number % 5 == 1 and wave_number != 1:
                    base_enemy_health += 10  # Zwiększenie bazowego zdrowia po falach z bossami

            # Sprawdzanie, czy gracz umarł
            if player.health <= 0:
                player.kill()
                print("Game Over! Final score:", kills_count)
                running = False
                game_over.game_over(kills_count, wave_number, f"{elapsed_time // 60}:{elapsed_time % 60:02d}", )

            # Aktualizacja ekranu
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    pygame.quit()

if __name__ == "__main__":
    main_game()