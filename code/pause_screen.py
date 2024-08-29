import sys
import pygame
import io
import settings
from main_menu import draw_text, main_menu


def show():
    font_title = pygame.font.Font(io.BytesIO(settings.font), int(60 * settings.h_scale))
    font_text = pygame.font.Font(io.BytesIO(settings.font), int(40 * settings.h_scale))
    font_button = pygame.font.Font(io.BytesIO(settings.font), int(20 * settings.h_scale))
    paused = True

    while paused:
        # Tworzenie przezroczystej powierzchni
        transparent_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        settings.screen.fill((0, 0, 0, 128))  # Czarny kolor z przezroczystością

        # Umieszczenie przezroczystej powierzchni na ekranie
        settings.screen.blit(transparent_surface, (0, 0))

        # Tekst na ekranie
        draw_text('Paused', font_title, settings.DARK_GREY, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 4)
        draw_text('Enemies are frozen, time is NOT!', font_text, settings.GREY, settings.screen,
                  settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 4 + int(80 * settings.h_scale))

        # Definicja przycisków
        button_continue = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale), settings.SCREEN_HEIGHT // 2, int(250 * settings.w_scale), int(50 * settings.h_scale))
        button_menu = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale), settings.SCREEN_HEIGHT // 2 + int(70 * settings.h_scale), int(250 * settings.w_scale), int(50 * settings.h_scale))

        pygame.draw.rect(settings.screen, settings.GREY, button_continue)
        pygame.draw.rect(settings.screen, settings.GREY, button_menu)

        draw_text('Continue', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 + int(25 * settings.h_scale))
        draw_text('Menu', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 + int(95 * settings.h_scale))

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
