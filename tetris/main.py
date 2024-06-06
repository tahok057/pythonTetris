import pygame
from game import Game
from colors import Colors
import sys

pygame.init()

# Setting up fonts and text surfaces
title_font = pygame.font.Font(None, 40)
menu_font = pygame.font.Font(None, 60)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
pause_surface = title_font.render("PAUSED", True, Colors.white)

# Setting up rectangles for score and next block display
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

# Setting up the display
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()
paused = False

# Setting up the custom event for game updates
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)


def main_menu():
    while True:
        screen.fill(Colors.dark_blue)
        title_surface = menu_font.render("Python Tetris", True, Colors.white)
        start_surface = menu_font.render("Start Game", True, Colors.white)
        quit_surface = menu_font.render("Quit Game", True, Colors.white)

        title_rect = title_surface.get_rect(center=(250, 150))
        start_rect = start_surface.get_rect(center=(250, 300))
        quit_rect = quit_surface.get_rect(center=(250, 400))

        screen.blit(title_surface, title_rect)
        screen.blit(start_surface, start_rect)
        screen.blit(quit_surface, quit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return  # Start the game
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


while True:
    main_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if not paused:
                    if game.game_over:
                        game.game_over = False
                        game.reset()
                    if event.key == pygame.K_LEFT and not game.game_over:
                        game.move_left()
                    if event.key == pygame.K_RIGHT and not game.game_over:
                        game.move_right()
                    if event.key == pygame.K_DOWN and not game.game_over:
                        game.move_down()
                        game.update_score(0, 1)
                    if event.key == pygame.K_UP and not game.game_over:
                        game.rotate()
                if event.key == pygame.K_p:
                    paused = not paused

            if event.type == GAME_UPDATE and not paused and not game.game_over:
                game.move_down()

        # Drawing
        score_value_surface = title_font.render(str(game.score), True, Colors.white)

        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (365, 20, 50, 50))
        screen.blit(next_surface, (375, 180, 50, 50))

        if game.game_over:
            screen.blit(game_over_surface, (320, 450, 50, 50))

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                      centery=score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)

        if paused and not game.game_over:
            screen.blit(pause_surface, (320, 450, 50, 50))

        pygame.display.update()
        clock.tick(60)
