import time
import pygame
import random
import math
import io
import settings
import death_screen
import pause_screen

from Player import Player
from Enemy import Enemy
from Bullet import Bullet
from HealthPotion import HealthPotion
from DamageBoost import DamageBoost
from HealthBoost import HealthBoost
from SpeedBoost import SpeedBoost

# Grupa sprite'ów
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
drops = pygame.sprite.Group()

# Kamera
camera = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

# Część ustawień gry
shot_interval = settings.shot_interval
boss_message_duration = settings.boss_message_duration
more_speed_message_duration = settings.more_speed_message_duration
boss_message_start_time = None
more_speed_message_start_time = None


# Główna pętla gry
def start():
    global boss_message_start_time
    global more_speed_message_start_time
    elapsed_time = None
    wave_number = 1
    kills_count = 0

    enemy_health = settings.enemy_health
    enemy_speed_change = settings.enemy_speed_change

    running = True
    paused = False

    waiting_for_next_wave = True
    wave_start_ticks = pygame.time.get_ticks()
    game_start_time = None
    left_mouse_button_down = False

    boss_message_start_time = None
    more_speed_message_start_time = None
    last_shot_time = 0

    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    drops.empty()

    background_surface = generate_background()
    player = Player()
    all_sprites.add(player)

    while running:
        current_time = time.time()  # Bieżący czas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen.show()  # Pauzujemy grę
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
            drops.update()

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
                        if hit_enemy.color == settings.BLACK:
                            drop_types = ['none']
                            weights = [1]
                            if player.max_health < settings.player_max_health_limit:
                                drop_types.append('health')
                                weights.append(settings.boost_chance)
                                weights[0] = weights[0] - settings.boost_chance
                            if player.damage < settings.player_damage_limit:
                                drop_types.append('damage')
                                weights.append(settings.boost_chance)
                                weights[0] = weights[0] - settings.boost_chance
                            if player.speed < settings.player_speed_limit:
                                drop_types.append('speed')
                                weights.append(settings.speed_chance)
                                weights[0] = weights[0] - settings.speed_chance

                            if weights[0] == 1:
                                drop_types = ['potion']

                            random_drop = random.choices(drop_types, weights)

                            if random_drop[0] == 'potion':
                                potion = HealthPotion(hit_enemy.rect.centerx, hit_enemy.rect.centery)
                                all_sprites.add(potion)
                                drops.add(potion)
                            if random_drop[0] == 'damage':
                                boost = DamageBoost(hit_enemy.rect.centerx, hit_enemy.rect.centery)
                                all_sprites.add(boost)
                                drops.add(boost)
                            if random_drop[0] == 'health':
                                boost = HealthBoost(hit_enemy.rect.centerx, hit_enemy.rect.centery)
                                all_sprites.add(boost)
                                drops.add(boost)
                            if random_drop[0] == 'speed':
                                boost = SpeedBoost(hit_enemy.rect.centerx, hit_enemy.rect.centery)
                                all_sprites.add(boost)
                                drops.add(boost)

                        # Jeśli zabiliśmy zwykłego przeciwnika
                        if hit_enemy.color == settings.RED:
                            drop = random.choices(['potion', 'none'],
                                                  [settings.drop_from_normal_enemy_chance,
                                                   1 - settings.drop_from_normal_enemy_chance])
                            if drop[0] == 'potion':
                                potion = HealthPotion(hit_enemy.rect.centerx, hit_enemy.rect.centery)
                                all_sprites.add(potion)
                                drops.add(potion)
                        hit_enemy.kill()
                        kills_count += 1

            # Sprawdzenie kolizji gracza z przedmiotem
            item_collected = pygame.sprite.spritecollideany(player, drops)
            if item_collected:
                if isinstance(item_collected, HealthPotion):
                    player.health = min(player.max_health, player.health + settings.healing_value)
                elif isinstance(item_collected, HealthBoost):
                    if player.max_health < settings.player_max_health_limit:
                        player.max_health += settings.health_boost_value
                elif isinstance(item_collected, DamageBoost):
                    if player.damage < settings.player_damage_limit:
                        player.damage += settings.damage_boost_value
                elif isinstance(item_collected, SpeedBoost):
                    if player.speed < settings.player_speed_limit:
                        player.speed += settings.speed_boost_value
                item_collected.kill()

            # Aktualizacja kamery
            camera.center = player.rect.center
            camera.clamp_ip(pygame.Rect(0, 0, settings.MAP_WIDTH, settings.MAP_HEIGHT))

            # Rysowanie
            draw_background(background_surface)
            for entity in all_sprites:
                settings.screen.blit(entity.image, (entity.rect.x - camera.x, entity.rect.y - camera.y))
                if isinstance(entity, Enemy):
                    draw_enemy_health_bar(entity)

            # Pasek obrażeń gracza
            font = pygame.font.Font(io.BytesIO(settings.font), int(17 * settings.h_scale))
            pygame.draw.rect(settings.screen, settings.BLACK,
                             (10, settings.SCREEN_HEIGHT - int(90 * settings.h_scale),
                              int((settings.player_damage_limit * 3 + 4) * settings.w_scale),
                              20), 2)
            pygame.draw.rect(settings.screen, settings.PURPLE,
                             (12, settings.SCREEN_HEIGHT - int(88 * settings.h_scale),
                              int(player.damage * 3 * settings.w_scale),
                              16))
            damage_text = font.render(f"{player.damage} DAMAGE", True, settings.BLACK)
            settings.screen.blit(damage_text, (int(((
                                                                settings.player_damage_limit * 1.5 + 10) - damage_text.get_width() // 2 - 1) * settings.w_scale), settings.SCREEN_HEIGHT - int(87 * settings.h_scale)))

            # Pasek szybkości gracza
            pygame.draw.rect(settings.screen, settings.BLACK,
                             (10, settings.SCREEN_HEIGHT - int(60 * settings.h_scale),
                              int((settings.player_damage_limit * 3 + 4) * settings.w_scale),
                              20), 2)
            pygame.draw.rect(settings.screen, settings.YELLOW,
                             (12, settings.SCREEN_HEIGHT - int(58 * settings.h_scale),
                              int((((
                                                settings.player_damage_limit * 3) / settings.player_speed_limit) * player.speed) * settings.w_scale),
                              16))
            speed_text = font.render(f"{player.speed} SPEED", True, settings.BLACK)
            settings.screen.blit(speed_text, (int(((
                                                               settings.player_damage_limit * 1.5 + 10) - speed_text.get_width() // 2) * settings.w_scale), settings.SCREEN_HEIGHT - int(57 * settings.h_scale)))

            # Pasek zdrowia gracza
            pygame.draw.rect(settings.screen, settings.BLACK,
                             (10, settings.SCREEN_HEIGHT - int(30 * settings.h_scale),
                              int((player.max_health * 3 + 4) * settings.w_scale),
                              20), 2)
            pygame.draw.rect(settings.screen, settings.GREEN,
                             (12, settings.SCREEN_HEIGHT - int(28 * settings.h_scale),
                              int(player.health * 3 * settings.w_scale),
                              16))
            health_text = font.render(f"{player.health}/{player.max_health} HEALTH", True, settings.BLACK)
            settings.screen.blit(health_text, (int(((player.max_health * 1.5 + 10) - health_text.get_width() // 2) * settings.w_scale), settings.SCREEN_HEIGHT - int(27 * settings.h_scale)))

            # Wyświetlanie informacji o fali i odliczaniu do następnej
            font = pygame.font.Font(io.BytesIO(settings.font), int(25 * settings.h_scale))
            wave_text = font.render((f"Wave {wave_number}" if game_start_time else f"Game") + (
                f" starting in {float('{:.1f}'.format((5050 - (pygame.time.get_ticks() - wave_start_ticks)) / 1000))}"
                if waiting_for_next_wave else ""), True, settings.BLACK)
            settings.screen.blit(wave_text, (int(10 * settings.w_scale), int(10 * settings.h_scale)))

            # Liczba pozostałych przeciwników
            enemies_left_text = font.render(f"Opponents left: {len(enemies)}" if not waiting_for_next_wave else "",
                                            True, settings.BLACK)
            settings.screen.blit(enemies_left_text, (int(10 * settings.w_scale), int(40 * settings.h_scale)))

            # Wyświetlanie czasu gry i licznika pokonanych przeciwników
            if game_start_time:
                elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000
                time_text = font.render(f"Time: {elapsed_time // 60}:{elapsed_time % 60:02d}", True, settings.BLACK)
                settings.screen.blit(time_text, (
                settings.SCREEN_WIDTH - time_text.get_width() - 5, int(10 * settings.h_scale)))

                kills_text = font.render(f'Kills: {kills_count}', True, settings.BLACK)
                settings.screen.blit(kills_text, (
                settings.SCREEN_WIDTH - kills_text.get_width() - 5, int(40 * settings.h_scale)))

            # Wyświetlanie komunikatu "BOSS incoming!"
            if boss_message_start_time:
                elapsed_boss_message_time = pygame.time.get_ticks() - boss_message_start_time
                if elapsed_boss_message_time < boss_message_duration:
                    settings.screen.fill(settings.BLACK, (0, int(100 * settings.h_scale), settings.SCREEN_WIDTH,
                                                          int(75 * settings.h_scale)))  # Czarne tło dla tekstu
                    current_time = pygame.time.get_ticks()
                    if current_time % 1000 < 300:  # Miganie tekstu
                        boss_text = pygame.font.Font(io.BytesIO(settings.font), int(60 * settings.h_scale)).render(
                            "BOSS INCOMING!",
                            True, settings.RED)
                        settings.screen.blit(boss_text, (
                        settings.SCREEN_WIDTH // 2 - boss_text.get_width() // 2, int(110 * settings.h_scale)))
                else:
                    boss_message_start_time = None

            # Wyświetlanie komunikatu "Enemy speed increased"
            if more_speed_message_start_time:
                elapsed_more_speed_message_time = pygame.time.get_ticks() - more_speed_message_start_time
                if elapsed_more_speed_message_time < more_speed_message_duration:
                    more_speed_text = pygame.font.Font(io.BytesIO(settings.font), int(40 * settings.h_scale)).render(
                        "Enemy speed increased",
                        True, settings.YELLOW)
                    settings.screen.blit(more_speed_text, (
                    settings.SCREEN_WIDTH // 2 - more_speed_text.get_width() // 2, int(110 * settings.h_scale)))
                else:
                    boss_message_start_time = None

            # Sprawdzenie, czy należy rozpocząć nową falę
            if waiting_for_next_wave and pygame.time.get_ticks() - wave_start_ticks >= 5000:
                waiting_for_next_wave = False
                generate_wave(wave_number, enemy_health, enemy_speed_change)
                if game_start_time is None:  # Ustawienie czasu rozpoczęcia gry przy pierwszej fali
                    game_start_time = pygame.time.get_ticks()

            # Jeśli fala się skończyła
            if not enemies and not waiting_for_next_wave:
                waiting_for_next_wave = True
                wave_number += 1
                wave_start_ticks = pygame.time.get_ticks()
                if wave_number % settings.x_waves_to_encrease_enemy_health == 1 and wave_number != 1:
                    enemy_health += settings.enemy_health_encrease_value
                if wave_number % settings.x_waves_to_encrease_enemy_speed == 1 and wave_number != 1:
                    enemy_speed_change += settings.enemy_speed_encrease_value

            # Sprawdzanie, czy gracz umarł
            if player.health <= 0:
                player.kill()
                running = False
                death_screen.show(kills_count, wave_number, elapsed_time // 60, elapsed_time % 60)

            # Aktualizacja ekranu
            pygame.display.flip()
            pygame.time.Clock().tick(settings.max_fps)
    pygame.quit()


# Funkcja generująca tło
def generate_background():
    background_surface = pygame.Surface((settings.MAP_WIDTH, settings.MAP_HEIGHT))
    tile_size = 50
    for y in range(0, settings.MAP_HEIGHT, tile_size):
        for x in range(0, settings.MAP_WIDTH, tile_size):
            tile_color = random.choice([settings.DARK_GREY, settings.LITTLE_DARK_GREY])
            pygame.draw.rect(background_surface, tile_color, pygame.Rect(x, y, tile_size, tile_size))
    return background_surface


# Funkcja rysująca tło
def draw_background(background_surface):
    settings.screen.blit(background_surface, (-camera.x, -camera.y))


# Funkcja rysująca pasek zdrowia przeciwników
def draw_enemy_health_bar(enemy):
    health_bar_width = 40
    health_bar_height = 5
    fill = (enemy.health / enemy.max_health) * health_bar_width
    outline_rect = pygame.Rect(enemy.rect.centerx - health_bar_width // 2 - camera.x,
                               enemy.rect.top - 15 - camera.y, health_bar_width, health_bar_height)
    fill_rect = pygame.Rect(enemy.rect.centerx - health_bar_width // 2 - camera.x, enemy.rect.top - 15 - camera.y,
                            fill, health_bar_height)
    pygame.draw.rect(settings.screen, settings.RED, fill_rect)
    pygame.draw.rect(settings.screen, settings.BLACK, outline_rect, 1)


# Funkcja generująca falę przeciwników
def generate_wave(wave_number, health, speed_change):
    global boss_message_start_time
    global more_speed_message_start_time
    num_enemies = wave_number % settings.max_enemies_spawn if not wave_number % settings.max_enemies_spawn == 0 else settings.max_enemies_spawn
    if wave_number % settings.x_waves_to_boss_wave == 0:  # Dodanie BOSSa
        num_enemies += 1
    for i in range(num_enemies):
        is_boss = True if wave_number % settings.x_waves_to_boss_wave == 0 and i == num_enemies - 1 else False
        health = (health * settings.boss_health_multiplier) if is_boss else health
        x = random.choice([random.randint(-100, 0), random.randint(settings.MAP_WIDTH, settings.MAP_WIDTH + 100)])
        y = random.choice([random.randint(-100, 0), random.randint(settings.MAP_HEIGHT, settings.MAP_HEIGHT + 100)])
        enemy = Enemy(x, y, health, speed_change, is_boss)
        all_sprites.add(enemy)
        enemies.add(enemy)

        # Komunikat "BOSS incoming!" na ekranie
        if is_boss:
            boss_message_start_time = pygame.time.get_ticks()

        # Komunikat "Enemy speed increased" na ekranie
        if wave_number % settings.x_waves_to_encrease_enemy_speed == 1 and wave_number != 1:
            more_speed_message_start_time = pygame.time.get_ticks()


# Wykrywanie kolizji między przeciwnikami
def resolve_enemy_collisions(all_enemies):
    for enemy in all_enemies:
        other_enemies = [e for e in all_enemies if e != enemy]
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


if __name__ == "__main__":
    pygame.init()
    start()
