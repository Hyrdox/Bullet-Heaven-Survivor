import pygame
import sys
import game
import top_scores

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
# Funkcja rysująca tekst na ekranie z opcją wyrównania do lewej
def draw_text(text, font, color, surface, x, y, align="center"):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if align == "center":
        textrect.center = (x, y)
    elif align == "left":
        textrect.midleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    font_title = pygame.font.Font('8514fixe.fon', 74)
    font_button = pygame.font.Font('8514fixe.fon', 50)

    while True:
        screen.fill(BLACK)

        # Rysowanie tytułu gry
        draw_text('Bullet Heaven Survivor', font_title, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # Definicja przycisków
        button_play = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 50, 250, 50)
        button_scores = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 20, 250, 50)
        button_exit = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 90, 250, 50)

        pygame.draw.rect(screen, GREY, button_play)
        pygame.draw.rect(screen, GREY, button_scores)
        pygame.draw.rect(screen, GREY, button_exit)

        draw_text('Play', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25)
        draw_text('Top scores', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 45)
        draw_text('Exit', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 115)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    game.main_game()  # Przejście do gry
                if button_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if button_scores.collidepoint(event.pos):
                    top_scores.top_scores()  # Przejście do ekranu z najlepszymi wynikami

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
