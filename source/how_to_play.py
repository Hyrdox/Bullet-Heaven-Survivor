import pygame
import sys
import io
import urllib
import settings
import main_menu

# Pobieranie obrazu z internetu
response = urllib.request.urlopen(settings.mouse_png_url)
image_data = response.read()

# Ładowanie obrazu z pamięci
image_file = io.BytesIO(image_data)
mouse_image = pygame.image.load(image_file)
mouse_image = pygame.transform.scale(mouse_image, (int(100 * settings.w_scale), int(100 * settings.w_scale)))


def how_to_play():
    font_title = pygame.font.Font(io.BytesIO(settings.font), int(60 * settings.w_scale))
    font_text = pygame.font.Font(io.BytesIO(settings.font), int(30 * settings.w_scale))
    font_button = pygame.font.Font(io.BytesIO(settings.font), int(20 * settings.w_scale))

    while True:
        settings.screen.fill(settings.BLACK)
        main_menu.draw_text('Welcome to ' + settings.game_title + '!', font_title, settings.RED, settings.screen,
                            settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 8)

        main_menu.draw_text(
            "Your goal is simple: survive as long as possible while fighting off waves of relentless enemies.",
            font_text, settings.LIGHT_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(40 * settings.h_scale), align="center")
        main_menu.draw_text(
            "Ready to take on the challenge? Here's everything you need to know to get started!",
            font_text, settings.LIGHT_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(75 * settings.h_scale), align="center")
        main_menu.draw_text(
            "Use the W, A, S, D keys to move your character around the battlefield.",
            font_text, settings.DARK_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(125 * settings.h_scale), align="center")
        main_menu.draw_text(
            "Aim with your mouse. Click or hold LPM to shoot.",
            font_text, settings.DARK_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(160 * settings.h_scale), align="center")

        draw_player_and_arrows()
        draw_mouse()

        main_menu.draw_text(
            "The game throws wave after wave of increasingly difficult enemies at you.",
            font_text, settings.LIGHT_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(300 * settings.h_scale), align="center")
        main_menu.draw_text(
            "Each wave grows stronger, faster, and more dangerous, so be prepared to adapt your strategy",
            font_text, settings.LIGHT_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(335 * settings.h_scale), align="center")
        main_menu.draw_text(
            "as the game progresses. Survive as many waves as you can!",
            font_text, settings.LIGHT_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(370 * settings.h_scale), align="center")
        main_menu.draw_text(
            "You start with a 100 health points. When enemies hit you, you lose 20 health.",
            font_text, settings.DARK_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(420 * settings.h_scale), align="center")
        main_menu.draw_text(
            "If your health reaches zero, it’s game over! Manage your health carefully",
            font_text, settings.DARK_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(455 * settings.h_scale), align="center")
        main_menu.draw_text(
            "and look out for health potions to restore your strength.",
            font_text, settings.DARK_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(490 * settings.h_scale), align="center")
        main_menu.draw_text(
            "Defeated enemies might drop power-ups. These can range from healing potions to health, damage",
            font_text, settings.LIGHT_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(540 * settings.h_scale), align="center")
        main_menu.draw_text(
            "or speed boosters. Keep an eye out for these drops - they could be the key to surviving longer.",
            font_text, settings.LIGHT_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(575 * settings.h_scale), align="center")
        main_menu.draw_text(
            "Your score will be determined by how many enemies you defeat and how long you survive.",
            font_text, settings.DARK_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(625 * settings.h_scale), align="center")
        main_menu.draw_text(
            "Compete to get your name on the leaderboard and aim for the top 10 best players!",
            font_text, settings.DARK_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(660 * settings.h_scale), align="center")
        main_menu.draw_text(
            "Jump into the fray and see how long you can survive. Good luck, and may your aim be true!",
            font_text, settings.LIGHT_GREY, settings.screen, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 7 + int(715 * settings.h_scale), align="center")

        # Przycisk "Main menu"
        button_main_menu = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale),
                                       settings.SCREEN_HEIGHT - ((settings.SCREEN_HEIGHT // 9) + int(25 * settings.h_scale)), int(250 * settings.w_scale), int(50 * settings.h_scale))
        pygame.draw.rect(settings.screen, settings.GREY, button_main_menu)
        main_menu.draw_text('Main menu', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                            settings.SCREEN_HEIGHT - (settings.SCREEN_HEIGHT // 9))

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_main_menu.collidepoint(event.pos):
                    return

        pygame.display.flip()


def draw_player_and_arrows():
    # Pozycja gracza (środek ekranu)
    player_pos = (settings.SCREEN_WIDTH // 9, settings.SCREEN_HEIGHT // 7 + int(200 * settings.h_scale))

    # Rysowanie gracza (zielone koło)
    pygame.draw.circle(settings.screen, settings.GREEN, player_pos, int(25 * settings.h_scale))

    # Odległość między graczem a literami
    arrow_length = int(50 * settings.h_scale)
    offset = int(5 * settings.h_scale)  # Dodatkowy odstęp od gracza i liter

    # Rysowanie strzałek i liter
    draw_arrow_and_text((player_pos[0], player_pos[1] - int(25 * settings.w_scale) - arrow_length), "W", "up", offset)
    draw_arrow_and_text((player_pos[0], player_pos[1] + int(25 * settings.w_scale) + arrow_length), "S", "down", offset)
    draw_arrow_and_text((player_pos[0] - int(25 * settings.h_scale) - arrow_length, player_pos[1]), "A", "left", offset)
    draw_arrow_and_text((player_pos[0] + int(25 * settings.h_scale) + arrow_length, player_pos[1]), "D", "right", offset)


# Funkcja rysująca strzałki i tekst na ich końcach
def draw_arrow_and_text(end_pos, text, direction, offset):
    player_pos = (settings.SCREEN_WIDTH // 9, settings.SCREEN_HEIGHT // 7 + int(200 * settings.h_scale))

    # Przesunięcie pozycji początkowej strzałek
    if direction == "up":
        start_pos = (player_pos[0], player_pos[1] - int(25 * settings.w_scale) - offset)
        adjusted_end_pos = (end_pos[0], end_pos[1] + int(10 * settings.w_scale) + offset)
        pygame.draw.line(settings.screen, settings.DARK_GREY, start_pos, adjusted_end_pos, 2)
        pygame.draw.polygon(settings.screen, settings.DARK_GREY, [(adjusted_end_pos[0], adjusted_end_pos[1] - 5),
                                                                  (adjusted_end_pos[0] - 5, adjusted_end_pos[1]),
                                                                  (adjusted_end_pos[0] + 5, adjusted_end_pos[1])])
    elif direction == "down":
        start_pos = (player_pos[0], player_pos[1] + int(25 * settings.w_scale) + offset)
        adjusted_end_pos = (end_pos[0], end_pos[1] - int(10 * settings.w_scale) - offset)
        pygame.draw.line(settings.screen, settings.DARK_GREY, start_pos, adjusted_end_pos, 2)
        pygame.draw.polygon(settings.screen, settings.DARK_GREY, [(adjusted_end_pos[0], adjusted_end_pos[1] + 5),
                                                                  (adjusted_end_pos[0] - 5, adjusted_end_pos[1]),
                                                                  (adjusted_end_pos[0] + 5, adjusted_end_pos[1])])
    elif direction == "left":
        start_pos = (player_pos[0] - int(25 * settings.h_scale) - offset, player_pos[1])
        adjusted_end_pos = (end_pos[0] + int(10 * settings.h_scale) + offset, end_pos[1])
        pygame.draw.line(settings.screen, settings.DARK_GREY, start_pos, adjusted_end_pos, 2)
        pygame.draw.polygon(settings.screen, settings.DARK_GREY, [(adjusted_end_pos[0] - 5, adjusted_end_pos[1]),
                                                                  (adjusted_end_pos[0], adjusted_end_pos[1] - 5),
                                                                  (adjusted_end_pos[0], adjusted_end_pos[1] + 5)])
    elif direction == "right":
        start_pos = (player_pos[0] + int(25 * settings.h_scale) + offset, player_pos[1])
        adjusted_end_pos = (end_pos[0] - int(10 * settings.h_scale) - offset, end_pos[1])
        pygame.draw.line(settings.screen, settings.DARK_GREY, start_pos, adjusted_end_pos, 2)
        pygame.draw.polygon(settings.screen, settings.DARK_GREY, [(adjusted_end_pos[0] + 5, adjusted_end_pos[1]),
                                                                  (adjusted_end_pos[0], adjusted_end_pos[1] - 5),
                                                                  (adjusted_end_pos[0], adjusted_end_pos[1] + 5)])

    # Rysowanie liter z dodatkowym marginesem
    draw_text(text, pygame.font.Font(io.BytesIO(settings.font), int(15 * settings.h_scale)), settings.GREY, end_pos[0], end_pos[1])


# Funkcja rysująca tekst
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    settings.screen.blit(text_surface, text_rect)


def draw_mouse():
    # Wyświetlanie obrazu myszy
    mouse_rect = mouse_image.get_rect(center=(settings.SCREEN_WIDTH // 9 * 8, settings.SCREEN_HEIGHT // 7 + int(200 * settings.h_scale)))
    settings.screen.blit(mouse_image, mouse_rect)
    draw_text('SHOOT', pygame.font.Font(io.BytesIO(settings.font), int(15 * settings.h_scale)), settings.GREY,
              settings.SCREEN_WIDTH // 9 * 8 - int(50 * settings.w_scale), settings.SCREEN_HEIGHT // 7 + int(175 * settings.h_scale))


if __name__ == "__main__":
    pygame.init()
