import pygame
import sys
import settings
import game
import top_scores


def main_menu():
    font_title = pygame.font.Font('8514fixe.fon', 74)
    font_button = pygame.font.Font('8514fixe.fon', 50)

    while True:
        settings.screen.fill(settings.BLACK)

        # Rysowanie tytułu gry
        draw_text('Bullet Heaven Survivor', font_title, settings.RED, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 4)

        # Definicja przycisków
        button_play = pygame.Rect(settings.SCREEN_WIDTH // 2 - 125, settings.SCREEN_HEIGHT // 2 - 50, 250, 50)
        button_scores = pygame.Rect(settings.SCREEN_WIDTH // 2 - 125, settings.SCREEN_HEIGHT // 2 + 20, 250, 50)
        button_exit = pygame.Rect(settings.SCREEN_WIDTH // 2 - 125, settings.SCREEN_HEIGHT // 2 + 90, 250, 50)

        pygame.draw.rect(settings.screen, settings.GREY, button_play)
        pygame.draw.rect(settings.screen, settings.GREY, button_scores)
        pygame.draw.rect(settings.screen, settings.GREY, button_exit)

        draw_text('Play', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 - 25)
        draw_text('Top scores', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 + 45)
        draw_text('Exit', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 + 115)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    game.start()  # Przejście do gry
                if button_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if button_scores.collidepoint(event.pos):
                    top_scores.top_scores()  # Przejście do ekranu z najlepszymi wynikami

        pygame.display.flip()


def draw_text(text, font, color, surface, x, y, align="center"):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if align == "center":
        textrect.center = (x, y)
    elif align == "left":
        textrect.midleft = (x, y)
    surface.blit(textobj, textrect)


if __name__ == "__main__":
    pygame.init()
    main_menu()
