'''
Game module
'''

from time import perf_counter
from board import Board


class Game:
    '''
    This class is used as a wrapper for the board class.
    It stores information about the time a game took to finish.
    '''

    def __init__(self, rows: int, cols: int, num_mines: int):
        self.__board: Board = Board(rows, cols, num_mines)
        self.__start_time: float = perf_counter()
        self.__end_time: float = perf_counter()

    def show(self, x: int, y: int):
        '''
        Shows a selected tile.
        If it was the first tile shown start the game timer.
        '''
        if self.should_continue():
            if not self.__board.has_started():
                self.__start_time = perf_counter()

            self.__board.show(x, y)

            if not self.__board.should_continue():
                self.__end_time = perf_counter()

    def toggle_marked(self, x: int, y: int):
        '''
        Marks/unmarks a tile if game is not over
        '''
        if self.should_continue():
            self.__board.toggle_marked(x, y)

    def should_continue(self) -> bool:
        '''
        Checks if any more moves are possible
        '''
        return self.__board.should_continue()

    def has_won(self) -> bool:
        '''
        Checks if the game was won
        '''
        return self.__board.has_won()

    def get_time(self) -> float:
        '''
        Gets the time it took to complete the game
        '''
        return self.__end_time - self.__start_time

    def print(self):
        '''
        Prints the board
        '''
        self.__board.print()

    def repr(self):
        '''
        Gets the board representation
        '''
        return self.__board.repr()
