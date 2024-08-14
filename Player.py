import pygame
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, settings.BLACK, (25, 25), 26)  # Border
        pygame.draw.circle(self.image, settings.GREEN, (25, 25), 25)
        self.rect = self.image.get_rect()
        self.rect.center = (settings.MAP_WIDTH // 2, settings.MAP_HEIGHT // 2)
        self.speed = settings.player_speed
        self.max_health = settings.player_max_health
        self.health = self.max_health
        self.damage = settings.player_damage

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < settings.MAP_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < settings.MAP_WIDTH:
            self.rect.x += self.speed

        # Miganie gracza po otrzymaniu obrażeń
        current_time = pygame.time.get_ticks()
        if hasattr(self, 'last_damage_time') and current_time - self.last_damage_time < settings.player_blinking_time:
            if current_time % 300 < 150:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)
