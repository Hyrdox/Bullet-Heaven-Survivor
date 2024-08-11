import pygame
import sys
import game

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Heaven Survivor")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
RED = (255, 0, 0)

# Funkcja rysująca tekst na ekranie
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def main_menu():
    font_title = pygame.font.Font(None, 74)
    font_button = pygame.font.Font(None, 50)

    while True:
        screen.fill(BLACK)

        # Rysowanie tytułu gry
        draw_text('Bullet Heaven Survivor', font_title, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # Definicja przycisków
        button_play = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        button_scores = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
        button_exit = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50)

        pygame.draw.rect(screen, GREY, button_play)
        pygame.draw.rect(screen, GREY, button_scores)
        pygame.draw.rect(screen, GREY, button_exit)

        draw_text('Play', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25)
        draw_text('Scores', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 45)
        draw_text('Exit', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 115)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    game.main_game()  # Przejście do gry
                    pass
                if button_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if button_scores.collidepoint(event.pos):
                    pass  # Obecnie bez funkcji

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
