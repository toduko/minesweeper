'''
GUI module
'''

import sys
import pygame

from src.ui.leaderboard_menu import LeaderboardMenu
from src.ui.difficulty_select import DifficultySelect
from src.ui.game_gui import GameGUI
from src.ui.screen import Screen
from src.ui.mouse import Mouse
from src.ui.menu_state import MenuState, State


class GUI:
    '''
    This class is used to play minesweeper with a graphical user interface.
    It has a menu for choosing a difficulty and leaderboards for difficulties with top scores.
    '''
    __difficulty_presets: dict[str, tuple[int, int, int]] = {"easy": (10, 10, 10), "medium": (
        16, 16, 40), "hard": (16, 30, 99)}
    __game_gui: GameGUI = GameGUI()
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

    def __back(self):
        '''
        Updates the state so that the next render the menu is shown
        '''
        self.__screen.set_menu_size(len(self.__difficulty_presets.keys()) + 1)

        if self.__state.get_state() == State.GAME:
            self.__game_gui.stop_game()
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
                    self.__back()
                if event.key == pygame.K_r and self.__state.get_state() == State.GAME:
                    self.__game_gui.restart()

        self.__mouse.handle_events()

        if self.__state.get_state() == State.GAME:
            self.__game_gui.render(self.__screen, self.__mouse)
        elif self.__state.get_state() == State.DIFFICULTY_SELECT:
            self.__difficulty_select.render(self.__screen,
                                            self.__mouse,
                                            self.__state,
                                            self.__difficulty_presets,
                                            self.__game_gui.start_game)
        else:
            self.__leaderboard_menu.render(self.__screen,
                                           self.__mouse,
                                           self.__state,
                                           self.__difficulty_presets)

        self.__mouse.cleanup()

        pygame.display.update()
