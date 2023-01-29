'''
GUI module
'''

import sys
import pygame

from src.utils import get_image_from_tile_char
from src.leaderboard_menu import LeaderboardMenu
from src.difficulty_select import DifficultySelect
from src.screen import Screen
from src.mouse import Mouse
from src.menu_state import MenuState, State
from src.game import Game
from src.text import Text


class GUI:
    '''
    This class is used to play minesweeper with a graphical user interface.
    It has a menu for choosing a difficulty and leaderboards for difficulties with top scores.
    '''
    __image_size: int = 32
    __last_state: list[list[str]] = None
    __game: Game = None
    __difficulty: str = ""
    __difficulty_presets: dict[str, tuple[int, int, int]] = {"easy": (10, 10, 10), "medium": (
        16, 16, 40), "hard": (16, 30, 99)}
    __leaderboard_menu: LeaderboardMenu = LeaderboardMenu()
    __screen: Screen = Screen()
    __mouse: Mouse = Mouse()
    __state: MenuState = MenuState()
    __difficulty_select: DifficultySelect = DifficultySelect()

    def __init__(self):
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        pygame.display.set_icon(pygame.image.load("assets/mine.png"))
        pygame.display.set_caption('Minesweeper')
        self.__screen.set_menu_size(
            (len(self.__difficulty_presets.keys()) + 1))

        while True:
            self.__render()

    def __render_game(self):
        '''
        Renders a minesweeper game on the screen
        '''
        state = self.__game.repr()

        x, y = self.__mouse.get_pos()
        x, y = x // self.__image_size, y // self.__image_size

        if self.__mouse.is_left_clicked():
            self.__game.show(x, y)

            if self.__game.has_won() and state != self.__game.repr():
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
                    f"assets/{get_image_from_tile_char(state[i][j])}.png")
                tile_rect = tile.get_rect()
                tile_rect.x, tile_rect.y = i * self.__image_size, j * self.__image_size
                self.__screen.get_screen().blit(tile, tile_rect)

        if not self.__game.should_continue():
            Text(self.__screen.get_width() // 2,
                 self.__screen.get_height() // 2,
                 f"You won! Your time is {self.__game.get_time():0.4f}s"
                 if self.__game.has_won(
            ) else "You lost").render(self.__screen)

        self.__last_state = state

    def __get_menu(self):
        '''
        Updates the state so that the next render the menu is shown
        '''
        self.__game = None
        self.__last_state = None
        self.__screen.set_menu_size(len(self.__difficulty_presets.keys()) + 1)

        if self.__state.get_state() == State.GAME:
            self.__state.set_state(State.DIFFICULTY_SELECT)
        elif self.__state.get_state() == State.LEADERBOARD:
            self.__state.set_state(State.LEADERBOARD_SELECT)

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
                    self.__game = Game((rows, cols, mines))

        self.__mouse.handle_events()

        if self.__state.get_state() == State.GAME:
            self.__render_game()
        elif self.__state.get_state() == State.DIFFICULTY_SELECT:
            self.__difficulty_select.render(self.__screen,
                                            self.__mouse,
                                            self.__state,
                                            self.__difficulty_presets,
                                            self.__start_game)

        else:
            self.__leaderboard_menu.render(self.__screen,
                                           self.__mouse,
                                           self.__state,
                                           self.__difficulty_presets)

        self.__mouse.cleanup()

        pygame.display.update()

    def __start_game(self, difficulty: str):
        '''
        Initializes a game according to the difficulty
        '''
        self.__state.set_state(State.GAME)
        self.__difficulty = difficulty
        rows, cols, mines = self.__difficulty_presets[difficulty]
        self.__screen.set_size(
            rows * self.__image_size, cols * self.__image_size)
        self.__game = Game((rows, cols, mines))
