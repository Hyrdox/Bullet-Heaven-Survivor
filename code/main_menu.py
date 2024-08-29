import pygame
import io
import sys
import requests
import settings
import game
import top_scores
import how_to_play
import no_connection


def main_menu():
    font_title = pygame.font.Font(io.BytesIO(settings.font), int(60 * settings.w_scale))
    font_button = pygame.font.Font(io.BytesIO(settings.font), int(20 * settings.w_scale))

    while True:
        settings.screen.fill(settings.BLACK)

        # Rysowanie tytułu gry
        draw_text(settings.game_title, font_title, settings.RED, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 4)

        # Definicja przycisków
        button_play = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale),
                                  settings.SCREEN_HEIGHT // 2, int(250 * settings.w_scale),
                                  int(50 * settings.h_scale))
        button_scores = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale),
                                    settings.SCREEN_HEIGHT // 2 + int(70 * settings.h_scale),
                                    int(250 * settings.w_scale), int(50 * settings.h_scale))
        button_how_to_play = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale),
                                         settings.SCREEN_HEIGHT // 2 + int(140 * settings.h_scale),
                                         int(250 * settings.w_scale), int(50 * settings.h_scale))
        button_exit = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale),
                                  settings.SCREEN_HEIGHT // 2 + int(210 * settings.h_scale),
                                  int(250 * settings.w_scale), int(50 * settings.h_scale))

        pygame.draw.rect(settings.screen, settings.GREY, button_play)
        pygame.draw.rect(settings.screen, settings.GREY, button_scores)
        pygame.draw.rect(settings.screen, settings.GREY, button_how_to_play)
        pygame.draw.rect(settings.screen, settings.GREY, button_exit)

        draw_text('Play', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 + int(25 * settings.h_scale))
        draw_text('Leaderboard', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 + int(95 * settings.h_scale))
        draw_text('How to play', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 + int(165 * settings.h_scale))
        draw_text('Exit', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                  settings.SCREEN_HEIGHT // 2 + int(235 * settings.h_scale))

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    game.start()
                if button_scores.collidepoint(event.pos):
                    top_scores.top_scores()
                if button_how_to_play.collidepoint(event.pos):
                    how_to_play.how_to_play()
                if button_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def draw_text(text, font, color, surface, x, y, align="center"):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if align == "center":
        textrect.center = (x, y)
    elif align == "left":
        textrect.midleft = (x, y)
    surface.blit(textobj, textrect)


def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


if __name__ == "__main__":
    pygame.init()
    if check_internet_connection():
        settings.programIcon = pygame.image.load(io.BytesIO(requests.get(settings.icon_url).content))
        pygame.display.set_icon(settings.programIcon)

        settings.font = requests.get(settings.font_url).content

        main_menu()
    else:
        no_connection.screen()
