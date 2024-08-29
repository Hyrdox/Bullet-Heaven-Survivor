import pygame
import sys
import settings
import main_menu


def screen():
    font_title = pygame.font.Font(settings.font, int(60 * settings.w_scale))
    font_text = pygame.font.Font(settings.font, int(40 * settings.h_scale))
    font_button = pygame.font.Font(settings.font, int(30 * settings.w_scale))

    while True:
        settings.screen.fill(settings.BLACK)

        main_menu.draw_text("No Internet connection!", font_title, settings.RED,
                            settings.screen,
                            settings.SCREEN_WIDTH // 2,
                            settings.SCREEN_HEIGHT // 4)

        main_menu.draw_text("Game requires Internet connection. Fix it and restart the game.", font_text, settings.GREY,
                            settings.screen,
                            settings.SCREEN_WIDTH // 2,
                            settings.SCREEN_HEIGHT // 4 * 2)

        button_exit = pygame.Rect(settings.SCREEN_WIDTH // 2 - int(125 * settings.w_scale),
                                  settings.SCREEN_HEIGHT - int(100 * settings.h_scale),
                                  int(250 * settings.w_scale), int(50 * settings.h_scale))
        pygame.draw.rect(settings.screen, settings.GREY, button_exit)
        main_menu.draw_text('Exit', font_button, settings.BLACK, settings.screen, settings.SCREEN_WIDTH // 2,
                            settings.SCREEN_HEIGHT - int(75 * settings.h_scale))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.collidepoint(event.pos):
                    return

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen()
