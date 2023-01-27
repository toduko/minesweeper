'''
Board module
'''

from itertools import product
from random import randint
from src.tile import Tile


class Board:
    '''
    This class represents a mxn board of tiles.
    It provides an interface for interacting with all of the tiles.
    '''

    def __init__(self, board_info: tuple[int, int, int] | list[list[Tile]]):
        self.__lose: bool = False
        self.__discovered: int = 0

        if isinstance(board_info, tuple):
            rows, cols, num_mines = board_info
            self.__rows: int = rows
            self.__cols: int = cols
            self.__num_mines: int = num_mines
            self.__started: bool = False
            self.__board: list[list[Tile | None]] = [[None
                                                      for _ in range(rows)] for _ in range(cols)]
            self.__neighbouring_mines: list[list[int]] = [
                [0 for _ in range(cols)] for _ in range(rows)]
            return

        self.__rows, self.__cols = len(board_info), len(board_info[0])
        self.__num_mines = sum(map(sum, [[1 if tile.is_mine()
                                          else 0 for tile in row]
                                         for row in board_info]))

        if not self.is_valid_board(self.__rows,
                                   self.__cols,
                                   self.__num_mines):
            raise Exception("Invalid board")

        self.__neighbouring_mines: list[list[int]] = [
            [0 for _ in range(self.__cols)] for _ in range(self.__rows)]
        self.__board = board_info
        self.__started = True
        self.__calculate_neighbouring_mines()

    def __begin_game(self, x: int, y: int):
        '''
        Starts a game from showing the board[x][y] tile.
        Bombs can't be placed near board[x][y].
        '''
        forbidden: tuple[int, int] = set()

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if self.__valid_coords(x + dx, y + dy):
                    forbidden.add((x + dx, y + dy))

        mine_coords = Board.generate_mine_coords(self.__rows,
                                                 self.__cols,
                                                 self.__num_mines,
                                                 forbidden)

        for i in range(self.__rows):
            for j in range(self.__cols):
                self.__board[i][j] = Tile((i, j) in mine_coords)

        self.__calculate_neighbouring_mines()

    def get_rows(self) -> int:
        '''
        Returns the amount of rows on the board
        '''
        return self.__rows

    def get_cols(self) -> int:
        '''
        Returns the amount of columns on the board
        '''
        return self.__cols

    def get_mines(self) -> int:
        '''
        Returns the amount of mines on the board
        '''
        return self.__num_mines

    def has_started(self) -> bool:
        '''
        Checks if the game has started (a tile was shown)
        '''
        return self.__started

    def has_won(self):
        '''
        Checks if the game was won
        '''
        return not (self.should_continue() or self.__lose)

    def should_continue(self):
        '''
        Checks if any more moves can be made
        '''
        return not self.__lose and self.__discovered != self.__rows * self.__cols - self.__num_mines

    def __calculate_neighbouring_mines(self):
        for x in range(self.__rows):
            for y in range(self.__cols):
                for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
                    if self.__valid_coords(
                        x + dx,
                        y + dy) \
                            and (dx, dy) != (0, 0) \
                            and self.__board[x][y] \
                            and self.__board[x][y].is_mine():
                        self.__neighbouring_mines[x + dx][y + dy] += 1

    @staticmethod
    def generate_mine_coords(rows: int,
                             cols: int,
                             num_mines: int,
                             forbidden: tuple[int, int]) -> set[tuple[int, int]]:
        '''
        Generates a fixed amount of mines on non-forbidden coordinates
        '''
        if rows * cols < num_mines or ((len(forbidden) + num_mines) / (rows * cols)) > 1:
            raise Exception("Invalid data")

        mine_coords: set[tuple[int, int]] = set()

        while len(mine_coords) < num_mines:
            x, y = randint(0, rows - 1), randint(0, cols - 1)
            if (x, y) not in forbidden:
                mine_coords.add((x, y))

        return mine_coords

    @staticmethod
    def is_valid_board(rows, cols: int, mines: int) -> bool:
        '''
        Checks if a board is valid.
        A board is valid if it is not too small and not full or empty of mines.
        '''
        return rows > 3 and cols > 3\
            and 0.1 <= (mines / (rows * cols)) <= 0.9\
            and rows * cols - mines > 9

    def __valid_coords(self, x: int, y: int) -> bool:
        '''
        Checks if coordinates are valid
        '''
        return 0 <= x < self.__rows and 0 <= y < self.__cols

    def __check_for_neighbours(self, x: int, y: int):
        '''
        Checks for neighbour tiles to possibly reveal them
        '''
        if not self.__valid_coords(x, y):
            return

        tile = self.__board[x][y]

        if tile.is_hidden() and not tile.is_marked():
            tile.show()
            self.__discovered += 1

            if tile.is_mine():
                self.__lose = True
            elif not self.__neighbouring_mines[x][y]:
                self.__show_neighbours(x, y)

    def __show_neighbours(self, x: int, y: int):
        '''
        Shows neighbouring tiles if possible
        '''
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != dy:
                    self.__check_for_neighbours(x + dx, y + dy)

    def show(self, x: int, y: int):
        '''
        Reveals a tile
        '''
        if not self.should_continue():
            return

        if not self.__started:
            self.__started = True
            self.__begin_game(x, y)

        self.__check_for_neighbours(x, y)

    def toggle_marked(self, x: int, y: int):
        '''
        Marks/unmarks a tile if possible
        '''
        if not self.should_continue() or not self.__valid_coords(x, y):
            return

        self.__board[x][y].toggle_marked()

    def __tile_repr(self, tile: Tile, x: int, y: int) -> str:
        if not tile:
            return '#'
        if tile.is_marked():
            return 'P'
        if tile.is_hidden():
            return '#'
        if tile.is_mine():
            return '*'

        return ' ' if not self.__neighbouring_mines[x][y]\
            else str(self.__neighbouring_mines[x][y])

    def print(self):
        '''
        Prints the board
        '''
        for row in self.repr():
            print(" ".join(row))

    def repr(self) -> list[list[str]]:
        '''
        Returns a mxn array of character representations of the tiles
        '''

        return [[self.__tile_repr(tile, row, col) for col, tile in enumerate(tile_row)]
                for row, tile_row in enumerate(self.__board)]
