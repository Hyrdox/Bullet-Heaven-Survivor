import pygame
import sys
import settings
import main_menu
from database import get_scores, reformat_data


def top_scores():
    font_title = pygame.font.Font('data/8514fixe.fon', 74)
    font_score = pygame.font.Font('data/8514fixe.fon', 40)
    font_button = pygame.font.Font('data/8514fixe.fon', 50)

    scores = reformat_data(get_scores())

    while True:
        settings.screen.fill(settings.BLACK)

        # Rysowanie tytułu
        main_menu.draw_text('Top Scores', font_title, settings.RED, settings.screen, settings.SCREEN_WIDTH // 2,
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
            main_menu.draw_text(text, font_score, settings.WHITE, settings.screen, x_position,
                                settings.SCREEN_HEIGHT // 7 + i * 40, align="left")

        # Definicja przycisku Back to menu
        button_back = pygame.Rect(settings.SCREEN_WIDTH // 2 - 150, settings.SCREEN_HEIGHT - 80, 300, 50)
        pygame.draw.rect(settings.screen, settings.GREY, button_back)
        main_menu.draw_text('Back to menu', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                            settings.SCREEN_HEIGHT - 55)

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
