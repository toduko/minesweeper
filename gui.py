'''
GUI module
'''

import sys
from typing import Callable
import pygame

from game import Game


class GUI:
    '''
    This class is used to play minesweeper with a graphical user interface.
    It has a menu for choosing a difficulty and leaderboards for difficulties with top scores.
    '''
    __image_size: int = 32
    __font_size: int = 20
    __left: bool = False
    __right: bool = False
    __timer_lclick: int = 0
    __timer_rclick: int = 0
    __last_state: list[list[str]] = None
    __lclick: bool = False
    __rclick: bool = False
    __game: Game = None
    __difficulty_presets: dict[str, tuple[int, int, int]] = {"easy": (10, 10, 10), "medium": (
        16, 16, 40), "hard": (16, 30, 99)}
    __leaderboard: str = None
    __leaderboard_list: bool = False
    __button_width: int = 240
    __button_height: int = 30
    __padding: int = 80
    __margin: int = 60
    __size: int = 0
    __width: int = 0
    __height: int = 0
    __screen: pygame.Surface = None

    def __init__(self):
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        pygame.display.set_icon(pygame.image.load("assets/mine.png"))
        pygame.display.set_caption('Minesweeper')
        self.__font = pygame.font.Font(
            pygame.font.get_default_font(), self.__font_size)
        self.__set_menu_size()

        while True:
            self.__render()

    def __render_button(self, y: int, title: str, on_click: Callable[[], None]):
        '''
        Renders a button on the screen
        '''
        pygame.draw.rect(self.__screen, (100, 100, 100), [
            self.__width // 2 - self.__button_width // 2, y - self.__button_height // 2, self.__button_width, self.__button_height])
        self.__render_text(y, title.capitalize())

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if (self.__width // 2 - self.__button_width // 2) <= mouse_x <= (self.__width // 2 + self.__button_width // 2)\
                and (y - self.__button_height // 2) <= mouse_y <= (y + self.__button_height // 2):
            if self.__lclick:
                on_click()

    def __handle_mouse(self):
        '''
        Handles mouse up/down events
        '''
        self.__left, _, self.__right = pygame.mouse.get_pressed()

        if self.__left:
            self.__timer_lclick += 1
        else:
            if self.__timer_lclick > 100:
                self.__lclick = True
            self.__timer_lclick = 0

        if self.__right:
            self.__timer_rclick += 1
        else:
            if self.__timer_rclick > 100:
                self.__rclick = True
            self.__timer_rclick = 0

    def __render_text(self, y: int, title: str):
        '''
        Renders text on screen
        '''
        text = self.__font.render(title, (0, 0, 0), (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.__width // 2, y)
        self.__screen.blit(text, text_rect)

    def __get_top_k_scores(self, k: int):
        '''
        Renders the top scores of screen
        '''
        self.__screen.fill((0, 0, 0))

        try:
            file = open(self.__leaderboard, "r")

            top_scores = sorted(list(map(float, filter(lambda x: x.replace(
                '.', '', 1).isdigit(), file.read().split("\n")))))[:k]
            if top_scores:
                self.__set_screen_size(
                    640, (len(top_scores) + 2) * (self.__margin // 2) + 2 * self.__padding)
                self.__render_text(
                    self.__padding, f"Top {self.__leaderboard} scores:")
                for i, score in enumerate(top_scores):
                    self.__render_text(
                        self.__padding + (i + 1) * self.__margin // 2, f"{i + 1} - {score:0.4f} seconds")
                self.__render_text(
                    self.__padding + (len(top_scores) + 2) * self.__margin // 2, "Press ESCAPE to go back")
            else:
                self.__render_text(
                    self.__height // 2 - self.__margin // 2, "No scores found for this difficulty")
                self.__render_text(
                    self.__height // 2 + self.__margin // 2, "Press ESCAPE to go back")
        except FileNotFoundError:
            self.__render_text(
                self.__height // 2 - self.__margin // 2, "No scores found for this difficulty")
            self.__render_text(
                self.__height // 2 + self.__margin // 2, "Press ESCAPE to go back")

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

        pos = pygame.mouse.get_pos()
        x, y = pos[0] // self.__image_size, pos[1] // self.__image_size

        if self.__lclick:
            self.__game.show(x, y)

            if not self.__game.should_continue() and self.__game.has_won() and state != self.__game.repr():
                time = self.__game.get_time()
                file = open(self.__difficulty, "a")
                file.write(str(time) + "\n")
                file.close()

        if self.__rclick:
            self.__game.toggle_marked(x, y)

        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__last_state and self.__last_state[i][j] == state[i][j]:
                    continue
                tile = pygame.image.load(
                    f"assets/{self.__get_image_from_tile_char(state[i][j])}.png")
                tile_rect = tile.get_rect()
                tile_rect.x, tile_rect.y = i * self.__image_size, j * self.__image_size
                self.__screen.blit(tile, tile_rect)

        if not self.__game.should_continue():
            self.__render_text(self.__height // 2, f"You won! Your time is {self.__game.get_time():0.4f}s" if self.__game.has_won(
            ) else "You lost")

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
            self.__render_button(
                self.__padding + i * self.__margin, difficulty, lambda: self.__start_game(difficulty))
        self.__render_button(self.__padding + len(self.__difficulty_presets.keys())
                             * self.__margin, "leaderboards", self.__toggle_list)

    def __render_list(self):
        '''
        Renders leaderboard list to the screen
        '''
        def set_leaderboard(difficulty: str):
            self.__leaderboard: str = difficulty

        for i, difficulty in enumerate(self.__difficulty_presets.keys()):
            self.__render_button(
                self.__padding + i * self.__margin, f"{difficulty} leaderboard", lambda: set_leaderboard(difficulty))
        self.__render_button(self.__padding + len(self.__difficulty_presets.keys())
                             * self.__margin, "back", self.__toggle_list)

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
                    self.__game = Game(self.__rows, self.__cols, self.__mines)

        self.__handle_mouse()
        if self.__game:
            self.__render_game()
        elif self.__leaderboard is not None:
            self.__render_leaderboard()
        elif self.__leaderboard_list:
            self.__render_list()
        else:
            self.__render_menu()

        self.__lclick = self.__rclick = False

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
        self.__rows, self.__cols, self.__mines = self.__difficulty_presets[self.__difficulty]
        self.__set_screen_size(
            self.__rows * self.__image_size, self.__cols * self.__image_size)
        self.__game = Game(self.__rows, self.__cols, self.__mines)
