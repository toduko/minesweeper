import sys
import pygame

from game import Game

pygame.init()

image_size = 32
font_size = 16
rows = 10
cols = 10
mines = 33

size = width, height = rows * image_size, cols * image_size
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Minesweeper')
time_left, time_right = 0, 0
game = Game(rows, cols, mines)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    left, _, right = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    x, y = pos[0] // image_size, pos[1] // image_size

    if left:
        time_left += 1
    else:
        if time_left > 10:
            game.show(x, y)

        time_left = 0

    if right:
        time_right += 1
    else:
        if time_right > 10:
            game.toggle_marked(x, y)
        time_right = 0

    state = game.repr()

    for i in range(rows):
        for j in range(cols):
            tile = pygame.image.load(f"assets/{state[i][j]}.png")
            tile_rect = tile.get_rect()
            tile_rect.x, tile_rect.y = i * image_size, j * image_size
            screen.blit(tile, tile_rect)

    if not game.should_continue():
        text = pygame.font.Font(pygame.font.get_default_font(), font_size).render("You won!" if game.has_won(
        ) else "You lost", (0, 0, 0), (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (width // 2, height // 2)
        screen.blit(text, text_rect)

    pygame.display.update()
