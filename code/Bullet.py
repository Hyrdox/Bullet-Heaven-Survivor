import pygame
import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, damage):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, settings.BLACK, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = settings.bullet_speed
        self.direction = direction
        self.damage = damage

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        if (self.rect.right < 0
                or self.rect.left > settings.MAP_WIDTH
                or self.rect.bottom < 0
                or self.rect.top > settings.MAP_HEIGHT):
            self.kill()
