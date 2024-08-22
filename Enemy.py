import pygame
import math
import settings


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, speed_change, is_boss=False):
        super().__init__()
        self.image = pygame.Surface((50, 50) if not is_boss else (60, 60), pygame.SRCALPHA)
        self.color = settings.BLACK if is_boss else settings.RED
        pygame.draw.circle(self.image, settings.BLACK, (25, 25) if not is_boss else (30, 30),
                           26 if not is_boss else 31)  # Border
        pygame.draw.circle(self.image, self.color, (25, 25) if not is_boss else (30, 30), 25 if not is_boss else 30)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_change = speed_change
        self.speed = self.speed_change + (settings.boss_speed if is_boss else settings.enemy_speed)
        self.max_health = health
        self.health = self.max_health
        self.damage = settings.enemy_damage
        self.knockback = settings.knockback

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
        player.health -= self.damage
        player.last_damage_time = pygame.time.get_ticks()

        # Odepchnięcie gracza
        player.rect.x += dx * self.knockback
        player.rect.y += dy * self.knockback
