import pygame
import io
import sys
import settings
import game
from main_menu import draw_text, main_menu
from database import get_scores, send_score, reformat_data


def show(kills, wave, minutes, seconds):
    font_title = pygame.font.Font(io.BytesIO(settings.font), int(60 * settings.h_scale))
    font_text = pygame.font.Font(io.BytesIO(settings.font), int(40 * settings.h_scale))
    font_button = pygame.font.Font(io.BytesIO(settings.font), int(20 * settings.h_scale))

    scores = reformat_data(get_scores())
    if len(scores) != 0:
        is_top_ten = False
        if kills > scores[-1][1]:
            is_top_ten = True
        if kills == scores[-1][1] and minutes * 60 + seconds < scores[-1][3] * 60 + scores[-1][4]:
            is_top_ten = True
        if len(scores) < 10:
            is_top_ten = True
    else:
        is_top_ten = True

    if not is_top_ten:
        while True:
            settings.screen.fill(settings.BLACK)
            draw_text('You died.', font_title, settings.RED, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 8)
            draw_text(f'Kills: {kills}', font_text, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + int(80 * settings.h_scale))
            draw_text(f'Wave: {wave}', font_text, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + int(140 * settings.h_scale))
            draw_text(f'Time: {minutes:02d}:{seconds:02d}', font_text, settings.WHITE, settings.screen,
                      settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 6 + int(200 * settings.h_scale))
            draw_text("That's not enough for TOP 10.", font_text, settings.WHITE, settings.screen,
                      settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 6 + int(260 * settings.h_scale))
            draw_text("Your score will not be saved. Try again.", font_text, settings.WHITE, settings.screen,
                      settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 6 + int(320 * settings.h_scale))

            # Przycisk "Try again"
            button_try_again = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(325 * settings.w_scale),
                                           settings.SCREEN_HEIGHT - int(80 * settings.h_scale),
                                           int(250 * settings.w_scale), int(50 * settings.h_scale))
            pygame.draw.rect(settings.screen, settings.GREY, button_try_again)
            draw_text('Try again', font_button, settings.BLACK, settings.screen,
                      settings.SCREEN_WIDTH // 2 - int(200 * settings.w_scale),
                      settings.SCREEN_HEIGHT - int(55 * settings.h_scale))

            # Przycisk "Main menu"
            button_main_menu = pygame.Rect(settings.SCREEN_WIDTH // 2 + int(25 * settings.w_scale),
                                           settings.SCREEN_HEIGHT - int(80 * settings.h_scale),
                                           int(250 * settings.w_scale), int(50 * settings.h_scale))
            pygame.draw.rect(settings.screen, settings.GREY, button_main_menu)
            draw_text('Main menu', font_button, settings.BLACK, settings.screen,
                      settings.SCREEN_WIDTH // 2 + int(200 * settings.w_scale),
                      settings.SCREEN_HEIGHT - int(55 * settings.h_scale))

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
        font_input = pygame.font.Font(io.BytesIO(settings.font), int(50 * settings.h_scale))
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
                      settings.SCREEN_HEIGHT // 6 + int(80 * settings.h_scale))
            draw_text(f'Wave: {wave}', font_text, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + int(140 * settings.h_scale))
            draw_text(f'Time: {minutes:02d}:{seconds:02d}', font_text, settings.WHITE, settings.screen,
                      settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 6 + int(200 * settings.h_scale))
            draw_text('Enter your name:', font_text, settings.WHITE, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + int(260 * settings.h_scale))

            # Pole tekstowe dla nicku
            input_box = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale),
                                    settings.SCREEN_HEIGHT // 6 + int(320 * settings.h_scale),
                                    int(250 * settings.w_scale), int(50 * settings.h_scale))
            pygame.draw.rect(settings.screen, settings.LIGHT_GREY, input_box)
            draw_text(nickname, font_input, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT // 6 + int(345 * settings.h_scale))

            # Przycisk "Submit"
            button_submit = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale),
                                        settings.SCREEN_HEIGHT - int(80 * settings.h_scale),
                                        int(250 * settings.w_scale), int(50 * settings.h_scale))
            pygame.draw.rect(settings.screen, settings.GREY, button_submit)
            draw_text('Submit', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                      settings.SCREEN_HEIGHT - int(55 * settings.h_scale))

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
