import pygame
import settings


class DamageBoost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.image, settings.BLACK, pygame.Rect(-1, -1, 31, 31))  # Border
        pygame.draw.rect(self.image, settings.PURPLE, pygame.Rect(0, 0, 30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Sprawdzanie czasu życia wzmocnienia
        elapsed_time = pygame.time.get_ticks() - self.spawn_time

        # Efekt migania
        if (settings.time_to_pickup - settings.blinking_time) <= elapsed_time <= settings.time_to_pickup:
            if elapsed_time // 250 % 2 == 0:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        elif elapsed_time > settings.time_to_pickup:
            self.kill()
