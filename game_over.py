import pygame
import sys
import time
import game
import menu
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

# Funkcja rysująca tekst na ekranie z opcją wyrównania do lewej
def draw_text(text, font, color, surface, x, y, align="center"):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if align == "center":
        textrect.center = (x, y)
    elif align == "left":
        textrect.midleft = (x, y)
    surface.blit(textobj, textrect)

def game_over(kills, wave, time_played):
    font_title = pygame.font.Font('8514fixe.fon', 74)
    font_text = pygame.font.Font('8514fixe.fon', 40)
    font_button = pygame.font.Font('8514fixe.fon', 50)

    scores = top_scores.load_scores()
    is_top_ten = True if kills > scores[-1][2] else True if len(scores) < 10 else False

    if not is_top_ten:
        while True:
            screen.fill(BLACK)
            draw_text('You died.', font_title, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8)
            draw_text(f'Kills: {kills}', font_text, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 80)
            draw_text(f'Wave: {wave}', font_text, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 140)
            draw_text(f'Time: {time_played}', font_text, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 200)
            draw_text("That's not enough for TOP 10.", font_text, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 260)
            draw_text("Your score will not be saved. Try again.", font_text, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 320)

            # Przycisk "Try again"
            button_try_again = pygame.Rect(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT - 80, 300, 50)
            pygame.draw.rect(screen, GREY, button_try_again)
            draw_text('Try again', font_button, WHITE, screen, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 55)

            # Przycisk "Main menu"
            button_main_menu = pygame.Rect(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT - 80, 300, 50)
            pygame.draw.rect(screen, GREY, button_main_menu)
            draw_text('Main menu', font_button, WHITE, screen, SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT - 55)

            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_try_again.collidepoint(event.pos):
                        game.main_game()
                    if button_main_menu.collidepoint(event.pos):
                        menu.main_menu()

            pygame.display.flip()

    else:
        placement = 1
        for score in scores:
            if kills > score[2]:
                input_nickname(kills, wave, time_played, placement)
            elif kills == score[2]:
                if time_played > score[2]:
                    placement += 1
                else:
                    input_nickname(kills, wave, time_played, placement)
            else:
                placement += 1
        input_nickname(kills, wave, time_played, placement)


def input_nickname(kills, wave, time_played, placement):
    font_title = pygame.font.Font('8514fixe.fon', 74)
    font_text = pygame.font.Font('8514fixe.fon', 40)
    font_input = pygame.font.Font('8514fixe.fon', 50)
    font_button = pygame.font.Font('8514fixe.fon', 50)

    nickname = ""
    active = True

    while active:
        screen.fill(BLACK)
        draw_text(f'You reached the TOP {placement}!', font_title, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8)
        draw_text(f'Kills: {kills}', font_text, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 80)
        draw_text(f'Wave: {wave}', font_text, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 140)
        draw_text(f'Time: {time_played}', font_text, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 200)
        draw_text('Enter your name:', font_text, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 260)

        # Pole tekstowe dla nicku
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 6 + 320, 300, 50)
        pygame.draw.rect(screen, GREY, input_box)
        draw_text(nickname, font_input, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 345)

        # Przycisk "Submit"
        button_submit = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 300, 50)
        pygame.draw.rect(screen, GREY, button_submit)
        draw_text('Submit', font_button, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 55)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                elif event.key == pygame.K_RETURN:
                    active = False  # Zakończ wprowadzanie i przejdź do zapisu
                else:
                    nickname += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_submit.collidepoint(event.pos):
                    active = False  # Zakończ wprowadzanie i przejdź do zapisu

        pygame.display.flip()

    # Zapis wyniku po zakończeniu wprowadzania nicku
    save_score(nickname, kills, wave, time_played)
    menu.main_menu()

def save_score(nickname, kills, wave, time_played):
    scores = top_scores.load_scores()  # Funkcja, która ładuje obecne wyniki
    scores.append((nickname, time_played, kills, wave))
    scores = sorted(scores, key=lambda x: (-x[2], x[1]))  # Sortowanie po kills, a potem po czasie
    scores = scores[:10]  # Trzymamy tylko TOP 10
    top_scores.update_scores(scores)


# Główna pętla gry
if __name__ == "__main__":
    game_over()
