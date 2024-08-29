import pygame
import settings


class SpeedBoost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, settings.BLACK, (15, 15), 16)  # Border
        pygame.draw.circle(self.image, settings.YELLOW, (15, 15), 15)
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
