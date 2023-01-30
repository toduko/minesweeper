'''
Game GUI module
'''

import pygame

from src.ui.menu_state import MenuState, State
from src.base.game import Game
from src.ui.text import Text
from src.ui.mouse import Mouse
from src.ui.screen import Screen


class GameGUI:
    '''
    This class is used to handle the base game graphical user interface
    '''
    __image_size: int = 32
    __last_state: list[list[str]] | None = None
    __game: Game | None = None
    __difficulty: str = ""

    def __get_image_from_tile_char(self, char: str):
        '''
        Get image filename from char representation of tile
        '''
        if char == '#':
            return "hidden"
        if char == 'P':
            return "flag"
        if char == '*':
            return "mine"
        if char == ' ':
            return "0"
        return char

    def render(self, screen: Screen, mouse: Mouse):
        '''
        Renders a minesweeper game on the screen
        '''
        state = self.__game.repr()

        x, y = mouse.get_pos()
        x, y = x // self.__image_size, y // self.__image_size

        if mouse.is_left_clicked():
            self.__game.show(x, y)

            if self.__game.has_won() and state != self.__game.repr():
                with open(self.__difficulty, "a", encoding="utf-8") as file:
                    file.write(str(self.__game.get_time()) + "\n")

        if mouse.is_right_clicked():
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
                screen.get_screen().blit(tile, tile_rect)

        if not self.__game.should_continue():
            Text(screen.get_width() // 2,
                 screen.get_height() // 2,
                 f"You won! Your time is {self.__game.get_time():0.4f}s"
                 if self.__game.has_won(
            ) else "You lost").render(screen)

        self.__last_state = state

    def start_game(self,
                   screen: Screen,
                   state: MenuState,
                   game_info: tuple[int, int, int],
                   difficulty: str):
        '''
        Initializes a game
        '''
        state.set_state(State.GAME)
        self.__difficulty = difficulty
        rows, cols, mines = game_info
        screen.set_size(
            rows * self.__image_size, cols * self.__image_size)
        self.__game = Game((rows, cols, mines))

    def stop_game(self):
        '''
        Stops the current game
        '''
        self.__game = None
        self.__last_state = None

    def restart(self):
        '''
        Restarts the game
        '''
        self.__last_state = None
        self.__game.restart()
