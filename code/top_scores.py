import pygame
import sys
import io
import settings
import main_menu
from database import get_scores, reformat_data


def top_scores():
    font_title = pygame.font.Font(io.BytesIO(settings.font), int(60 * settings.h_scale))
    font_score = pygame.font.Font(io.BytesIO(settings.font), int(40 * settings.h_scale))
    font_button = pygame.font.Font(io.BytesIO(settings.font), int(20 * settings.h_scale))

    scores = reformat_data(get_scores())

    while True:
        settings.screen.fill(settings.BLACK)

        # Rysowanie tytułu
        main_menu.draw_text('Leaderboard', font_title, settings.RED, settings.screen, settings.SCREEN_WIDTH // 2,
                            settings.SCREEN_HEIGHT // 9)

        # Obliczenie szerokości najdłuższego tekstu dla wyrównania do lewej
        max_width = 0 if len(scores) == 0 else max(
            font_score.size(f"{i}. {nick} - {kills} kills, wave {wave} ({minutes:02d}:{seconds:02d})")[0] for
            i, (nick, kills, wave, minutes, seconds) in enumerate(scores, start=1))

        # Pozycja X dla wyrównania listy do lewej, ale na środku ekranu
        x_position = (settings.SCREEN_WIDTH - max_width) // 2

        # Rysowanie listy wyników
        for i, (nick, kills, wave, minutes, seconds) in enumerate(scores, start=1):
            text = (f" " if i < 10 else "") + f"{i}. {nick} - {kills} kills, wave {wave} ({minutes:02d}:{seconds:02d})"
            main_menu.draw_text(text, font_score, settings.LIGHT_GREY, settings.screen, x_position,
                                settings.SCREEN_HEIGHT // 7 + int(i * 60 * settings.h_scale), align="left")

        # Definicja przycisku Back to menu
        button_back = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale),
                                  settings.SCREEN_HEIGHT - ((settings.SCREEN_HEIGHT // 9) + int(25 * settings.h_scale)),
                                  int(250 * settings.w_scale), int(50 * settings.h_scale))
        pygame.draw.rect(settings.screen, settings.GREY, button_back)
        main_menu.draw_text('Back to menu', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                            settings.SCREEN_HEIGHT - (settings.SCREEN_HEIGHT // 9))

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.collidepoint(event.pos):
                    return  # Powrót do menu głównego

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
