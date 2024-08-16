import sys
import pygame
import settings
from main_menu import draw_text, main_menu


def show():
    font_button = pygame.font.Font('data/8514fixe.fon', 50)
    paused = True

    while paused:
        # Tworzenie przezroczystej powierzchni
        transparent_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 128))  # Czarny kolor z przezroczystością

        # Umieszczenie przezroczystej powierzchni na ekranie
        settings.screen.blit(transparent_surface, (0, 0))

        # Tekst na ekranie
        draw_text('Paused', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 4)
        draw_text('Enemies are frozen, time is NOT', font_button, settings.GREY, settings.screen,
                  settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 4 + 40)

        # Definicja przycisków
        button_continue = pygame.Rect(settings.SCREEN_WIDTH // 2 - 125, settings.SCREEN_HEIGHT // 2 - 50, 250, 50)
        button_menu = pygame.Rect(settings.SCREEN_WIDTH // 2 - 125, settings.SCREEN_HEIGHT // 2 + 20, 250, 50)

        pygame.draw.rect(settings.screen, settings.GREY, button_continue)
        pygame.draw.rect(settings.screen, settings.GREY, button_menu)

        draw_text('Continue', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 - 25)
        draw_text('Menu', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 + 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_continue.collidepoint(event.pos):
                    paused = False  # Wracamy do gry
                if button_menu.collidepoint(event.pos):
                    main_menu()  # Powrót do menu głównego
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False  # Wracamy do gry

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
