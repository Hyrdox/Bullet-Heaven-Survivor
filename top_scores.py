import pygame
import sys
import requests
import menu

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

scores = [("AAA", "01:30", 40, 6), ("BBB", "01:15", 30, 6), ("CCC", "1:00", 20, 5)]  # Domyślne wyniki

def load_scores():
    return scores

def update_scores(new_scores):
    global scores
    scores = new_scores

def top_scores():
    font_title = pygame.font.Font('8514fixe.fon', 74)
    font_score = pygame.font.Font('8514fixe.fon', 40)
    font_button = pygame.font.Font('8514fixe.fon', 50)

    scores = load_scores()

    while True:
        screen.fill(BLACK)

        # Rysowanie tytułu
        menu.draw_text('Top Scores', font_title, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 9)

        # Obliczenie szerokości najdłuższego tekstu dla wyrównania do lewej
        max_width = max(font_score.size(f"{i}. {nick} - {kills} kills, wave {wave} ({time})")[0] for i, (nick, time, kills, wave) in
                        enumerate(scores, start=1))

        # Pozycja X dla wyrównania listy do lewej, ale na środku ekranu
        x_position = (SCREEN_WIDTH - max_width) // 2

        # Rysowanie listy wyników
        for i, (nick, time, kills, wave) in enumerate(scores, start=1):
            text = ((f" ") if i < 10 else "") + f"{i}. {nick} - {kills} kills, wave {wave} ({time})"
            menu.draw_text(text, font_score, WHITE, screen, x_position, SCREEN_HEIGHT // 7 + i * 40, align="left")

        # Definicja przycisku Back to menu
        button_back = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 300, 50)
        pygame.draw.rect(screen, GREY, button_back)
        menu.draw_text('Back to menu', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 55)

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
    top_scores()