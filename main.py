import pygame
import random
import math

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra 2D")

# Ustawienia mapy
MAP_WIDTH, MAP_HEIGHT = 1600, 1200

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.speed = 5
        self.health = 100

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < MAP_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < MAP_WIDTH:
            self.rect.x += self.speed


# Klasa przeciwnika
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.health = 20

    def update(self, player):
        # Przesunięcie w stronę gracza
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Sprawdzenie kolizji z pociskami
        if pygame.sprite.spritecollideany(self, bullets):
            self.health -= 10
            if self.health <= 0:
                self.kill()


# Klasa pocisku
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        if self.rect.right < 0 or self.rect.left > MAP_WIDTH or self.rect.bottom < 0 or self.rect.top > MAP_HEIGHT:
            self.kill()


# Grupa sprite'ów
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Inicjalizacja gracza
player = Player()
all_sprites.add(player)

# Dodanie kilku przeciwników
for _ in range(5):
    x = random.choice([random.randint(-100, 0), random.randint(MAP_WIDTH, MAP_WIDTH + 100)])
    y = random.choice([random.randint(-100, 0), random.randint(MAP_HEIGHT, MAP_HEIGHT + 100)])
    enemy = Enemy(x, y)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Kamera
camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Strzelanie
            direction = pygame.mouse.get_pos()[0] - SCREEN_WIDTH // 2, pygame.mouse.get_pos()[1] - SCREEN_HEIGHT // 2
            dist = math.hypot(*direction)
            direction = direction[0] / dist, direction[1] / dist
            bullet = Bullet(player.rect.centerx, player.rect.centery, direction)
            all_sprites.add(bullet)
            bullets.add(bullet)

    # Aktualizacja
    keys = pygame.key.get_pressed()
    player.update(keys)  # Aktualizacja pozycji gracza
    for enemy in enemies:
        enemy.update(player)  # Aktualizacja pozycji przeciwników w oparciu o pozycję gracza
    bullets.update()

    # Aktualizacja kamery
    camera.center = player.rect.center
    camera.clamp_ip(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))

    # Rysowanie
    screen.fill(BLACK)
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera.x, sprite.rect.y - camera.y))

    # Wyświetlanie ekranu
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
