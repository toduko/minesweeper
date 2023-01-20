'''
GUI module
'''

import sys
import pygame

from button import Button
from mouse import Mouse
from game import Game
from text import Text


class GUI:
    '''
    This class is used to play minesweeper with a graphical user interface.
    It has a menu for choosing a difficulty and leaderboards for difficulties with top scores.
    '''
    __image_size: int = 32
    __last_state: list[list[str]] = None
    __game: Game = None
    __difficulty_presets: dict[str, tuple[int, int, int]] = {"easy": (10, 10, 10), "medium": (
        16, 16, 40), "hard": (16, 30, 99)}
    __leaderboard: str = None
    __leaderboard_list: bool = False
    __padding: int = 80
    __margin: int = 60
    __size: int = 0
    __width: int = 0
    __height: int = 0
    __screen: pygame.Surface = None
    __mouse: Mouse = Mouse()

    def __init__(self):
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        pygame.display.set_icon(pygame.image.load("assets/mine.png"))
        pygame.display.set_caption('Minesweeper')
        self.__set_menu_size()

        while True:
            self.__render()

    def __get_top_k_scores(self, k: int):
        '''
        Renders the top scores of screen
        '''
        self.__screen.fill((0, 0, 0))

        try:
            with open(self.__leaderboard, "r", encoding="utf-8") as file:
                top_scores = sorted(list(map(float, filter(lambda x: x.replace(
                    '.', '', 1).isdigit(), file.read().split("\n")))))[:k]

                if not top_scores:
                    raise LookupError

                self.__set_screen_size(
                    640, (len(top_scores) + 2) * (self.__margin // 2) + 2 * self.__padding)
                Text(self.__width // 2,
                     self.__padding, f"Top {self.__leaderboard} scores:").render(self.__screen)
                for i, score in enumerate(top_scores):
                    Text(self.__width // 2,
                         self.__padding + (i + 1) * self.__margin // 2, f"{i + 1} - {score:0.4f} seconds").render(self.__screen)
                Text(self.__width // 2,
                     self.__padding + (len(top_scores) + 2) * self.__margin // 2, "Press ESCAPE to go back").render(self.__screen)
        except (FileNotFoundError, LookupError):
            Text(self.__width // 2,
                 self.__height // 2 - self.__margin // 2, "No scores found for this difficulty").render(self.__screen)
            Text(self.__width // 2,
                 self.__height // 2 + self.__margin // 2, "Press ESCAPE to go back").render(self.__screen)

    def __get_image_from_tile_char(self, char: str):
        '''
        Get image filename from char representation of tile
        '''
        if char == '#':
            return "hidden"
        elif char == 'P':
            return "flag"
        elif char == '*':
            return "mine"
        elif char == ' ':
            return "0"
        else:
            return char

    def __render_game(self):
        '''
        Renders a minesweeper game on the screen
        '''
        state = self.__game.repr()

        x, y = self.__mouse.get_pos()
        x, y = x // self.__image_size, y // self.__image_size

        if self.__mouse.is_left_clicked():
            self.__game.show(x, y)

            if not self.__game.should_continue() and self.__game.has_won() and state != self.__game.repr():
                with open(self.__difficulty, "a", encoding="utf-8") as file:
                    file.write(str(self.__game.get_time()) + "\n")

        if self.__mouse.is_right_clicked():
            self.__game.toggle_marked(x, y)

        rows, cols = self.__game.get_dimensions()

        for i in range(rows):
            for j in range(cols):
                if self.__last_state and self.__last_state[i][j] == state[i][j]:
                    continue
                tile = pygame.image.load(
                    f"assets/{self.__get_image_from_tile_char(state[i][j])}.png")
                tile_rect = tile.get_rect()
                tile_rect.x, tile_rect.y = i * self.__image_size, j * self.__image_size
                self.__screen.blit(tile, tile_rect)

        if not self.__game.should_continue():
            Text(self.__width // 2, self.__height // 2, f"You won! Your time is {self.__game.get_time():0.4f}s" if self.__game.has_won(
            ) else "You lost").render(self.__screen)

        self.__last_state = state

    def __toggle_list(self):
        '''
        Toggles whether the leaderboards list is shown or not
        '''
        self.__leaderboard_list ^= True

    def __render_menu(self):
        '''
        Renders game menu to the screen
        '''
        for i, difficulty in enumerate(self.__difficulty_presets.keys()):
            Button(self.__width // 2,
                   self.__padding + i * self.__margin,
                   difficulty,
                   lambda: self.__start_game(difficulty)).render(self.__screen, self.__mouse)
        Button(self.__width // 2,
               self.__padding +
               len(self.__difficulty_presets.keys()) * self.__margin,
               "leaderboards",
               self.__toggle_list).render(self.__screen, self.__mouse)

    def __render_list(self):
        '''
        Renders leaderboard list to the screen
        '''
        def set_leaderboard(difficulty: str):
            self.__leaderboard: str = difficulty

        for i, difficulty in enumerate(self.__difficulty_presets.keys()):
            Button(self.__width // 2,
                   self.__padding + i * self.__margin,
                   f"{difficulty} leaderboard",
                   lambda: set_leaderboard(difficulty)).render(self.__screen, self.__mouse)
        Button(self.__width // 2,
               self.__padding +
               len(self.__difficulty_presets.keys()) * self.__margin,
               "back",
               self.__toggle_list).render(self.__screen, self.__mouse)

    def __get_menu(self):
        '''
        Updates the state so that the next render the menu is shown
        '''
        self.__game = None
        self.__last_state = None
        self.__leaderboard = None
        self.__set_menu_size()

    def __render_leaderboard(self):
        '''
        Renders leaderboard to the screen
        '''
        self.__get_top_k_scores(10)

    def __set_menu_size(self):
        '''
        Sets the screen size to fit the menu
        '''
        self.__set_screen_size(
            640, self.__padding * 2 + (len(self.__difficulty_presets.keys()) + 1) * self.__margin)

    def __render(self):
        '''
        Renders everything to the screen
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.__get_menu()

                if event.key == pygame.K_r and self.__game:
                    rows, cols, mines = self.__difficulty_presets[self.__difficulty]
                    self.__game = Game(rows, cols, mines)

        self.__mouse.handle_events()

        if self.__game:
            self.__render_game()
        elif self.__leaderboard is not None:
            self.__render_leaderboard()
        elif self.__leaderboard_list:
            self.__render_list()
        else:
            self.__render_menu()

        self.__mouse.cleanup()

        pygame.display.update()

    def __set_screen_size(self, width: int, height: int):
        '''
        Sets screen size
        '''
        self.__size = self.__width, self.__height = width, height
        self.__screen = pygame.display.set_mode(self.__size)

    def __start_game(self, difficulty: str):
        '''
        Initializes a game according to the difficulty
        '''
        self.__difficulty = difficulty
        rows, cols, mines = self.__difficulty_presets[difficulty]
        self.__set_screen_size(
            rows * self.__image_size, cols * self.__image_size)
        self.__game = Game(rows, cols, mines)
