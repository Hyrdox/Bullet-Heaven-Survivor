import pygame
import settings


class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, settings.BLACK, [(15, -3), (33, 33), (-3, 33)])  # Border
        pygame.draw.polygon(self.image, settings.GREEN, [(15, 0), (30, 30), (0, 30)])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Sprawdzanie czasu życia mikstury
        elapsed_time = pygame.time.get_ticks() - self.spawn_time

        # Efekt migania
        if (settings.time_to_pickup - settings.blinking_time) <= elapsed_time <= settings.time_to_pickup:
            if elapsed_time // 250 % 2 == 0:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        elif elapsed_time > settings.time_to_pickup:
            self.kill()
