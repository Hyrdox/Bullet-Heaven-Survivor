import pygame
import sys
import settings
import game
from main_menu import draw_text, main_menu
from database import get_scores, send_score, reformat_data


def show(kills, wave, minutes, seconds):
    font_title = pygame.font.Font(settings.font, 74)
    font_text = pygame.font.Font(settings.font, 40)
    font_button = pygame.font.Font(settings.font, 50)

    scores = reformat_data(get_scores())
    if len(scores) != 0:
        is_top_ten = True if kills > scores[-1][1] else True if len(scores) < 10 else False
    else:
        is_top_ten = True

    if not is_top_ten:
        while True:
            settings.screen.fill(settings.BLACK)
            draw_text('You died.', font_title, settings.RED, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 8)
            draw_text(f'Kills: {kills}', font_text, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + 80)
            draw_text(f'Wave: {wave}', font_text, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + 140)
            draw_text(f'Time: {minutes:02d}:{seconds:02d}', font_text, settings.WHITE, settings.screen,
                      settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 6 + 200)
            draw_text("That's not enough for TOP 10.", font_text, settings.WHITE, settings.screen,
                      settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 6 + 260)
            draw_text("Your score will not be saved. Try again.", font_text, settings.WHITE, settings.screen,
                      settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 6 + 320)

            # Przycisk "Try again"
            button_try_again = pygame.Rect(settings.SCREEN_WIDTH // 2 - 350, settings.SCREEN_HEIGHT - 80, 300, 50)
            pygame.draw.rect(settings.screen, settings.GREY, button_try_again)
            draw_text('Try again', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2 - 200,
                      settings.SCREEN_HEIGHT - 55)

            # Przycisk "Main menu"
            button_main_menu = pygame.Rect(settings.SCREEN_WIDTH // 2 + 50, settings.SCREEN_HEIGHT - 80, 300, 50)
            pygame.draw.rect(settings.screen, settings.GREY, button_main_menu)
            draw_text('Main menu', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2 + 200,
                      settings.SCREEN_HEIGHT - 55)

            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_try_again.collidepoint(event.pos):
                        game.start()
                    if button_main_menu.collidepoint(event.pos):
                        main_menu()

            pygame.display.flip()
    else:
        font_input = pygame.font.Font(settings.font, 50)
        nickname = ""

        # Obliczanie zajętego przez gracza miejsca
        placement = 1
        for score in scores:
            if kills > score[1]:
                break
            elif kills == score[1]:
                if minutes * 60 + seconds > score[3] * 60 + score[4]:
                    placement += 1
                else:
                    break
            else:
                placement += 1

        while True:
            settings.screen.fill(settings.BLACK)
            draw_text(f'You reached the TOP {placement}!', font_title, settings.RED, settings.screen,
                      settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 8)
            draw_text(f'Kills: {kills}', font_text, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + 80)
            draw_text(f'Wave: {wave}', font_text, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + 140)
            draw_text(f'Time: {minutes:02d}:{seconds:02d}', font_text, settings.WHITE, settings.screen,
                      settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 6 + 200)
            draw_text('Enter your name:', font_text, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + 260)

            # Pole tekstowe dla nicku
            input_box = pygame.Rect(settings.SCREEN_WIDTH // 2 - 150, settings.SCREEN_HEIGHT // 6 + 320, 300, 50)
            pygame.draw.rect(settings.screen, settings.GREY, input_box)
            draw_text(nickname, font_input, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + 345)

            # Przycisk "Submit"
            button_submit = pygame.Rect(settings.SCREEN_WIDTH // 2 - 150, settings.SCREEN_HEIGHT - 80, 300, 50)
            pygame.draw.rect(settings.screen, settings.GREY, button_submit)
            draw_text('Submit', font_button, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT - 55)

            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    elif event.key == pygame.K_RETURN:
                        send_score(nickname, kills, wave, minutes, seconds)
                        main_menu()
                    else:
                        nickname += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_submit.collidepoint(event.pos):
                        send_score(nickname, kills, wave, minutes, seconds)
                        main_menu()

            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
