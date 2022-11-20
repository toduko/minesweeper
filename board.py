from random import randint
from tile import Tile


class Board:
    def __init__(self, rows, cols, num_mines):
        if not self.is_valid_board(rows, cols, num_mines):
            raise Exception("Invalid board")

        self.__rows = rows
        self.__cols = cols
        self.__num_mines = num_mines
        self.__started = False
        self.__lose = False
        self.__discovered = 0

        self.__board = [[Tile()
                         for _ in range(self.__cols)] for _ in range(self.__rows)]

    def __begin_game(self, x, y):
        self.__forbidden = set()

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if self.__valid_coords(x + dx, y + dy):
                    self.__forbidden.add((x + dx, y + dy))

        mine_coords = self.__generate_mine_coords()

        for x in range(self.__rows):
            for y in range(self.__cols):
                if (x, y) in mine_coords:
                    self.__board[x][y].set_mine()

        self.__calculate_neighbour_mines()

    def get_rows(self):
        return self.__rows

    def get_cols(self):
        return self.__cols

    def get_mines(self):
        return self.__num_mines

    def has_started(self):
        return self.__started

    def has_won(self):
        return not (self.should_continue() or self.__lose)

    def should_continue(self):
        return not self.__lose and self.__discovered != self.__rows * self.__cols - self.__num_mines

    def __calculate_neighbour_mines(self):
        for x in range(self.__rows):
            for y in range(self.__cols):
                count = 0

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (dx, dy) != (0, 0) and \
                            self.__valid_coords(x + dx, y + dy) and \
                                self.__board[x + dx][y + dy].is_mine():
                            count += 1

                self.__board[x][y].set_neighbour_mines(count)

    def __generate_mine_coords(self):
        mine_coords = set()

        while len(mine_coords) < self.__num_mines:
            x, y = randint(0, self.__rows - 1), randint(0, self.__cols - 1)
            if (x, y) not in self.__forbidden:
                mine_coords.add((x, y))

        return mine_coords

    @staticmethod
    def is_valid_board(rows, cols, mines):
        return rows > 3 and cols > 3\
            and 0.1 <= (mines / (rows * cols)) <= 0.9\
            and rows * cols - mines > 9

    def __valid_coords(self, x, y):
        return 0 <= x < self.__rows and 0 <= y < self.__cols

    def __check_for_neighbours(self, x, y):
        if not self.__valid_coords(x, y):
            return

        tile = self.__board[x][y]

        if not tile.is_hidden():
            print("Tile already shown")

        if tile.is_marked():
            print("Cannot show a marked tiles")

        if tile.is_hidden() and not tile.is_marked():
            tile.show()
            self.__discovered += 1

            if tile.is_mine():
                self.__lose = True
            elif not tile.get_neighbour_mines():
                self.__show_neighbours(x, y)

    def __show_neighbours(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx != dy):
                    self.__check_for_neighbours(x + dx, y + dy)

    def show(self, x, y):
        if not self.should_continue():
            return

        if not self.__started:
            self.__started = True
            self.__begin_game(x, y)

        self.__check_for_neighbours(x, y)

    def toggle_marked(self, x, y):
        if not self.should_continue() or not self.__valid_coords(x, y):
            return

        self.__board[x][y].toggle_marked()

    def print(self):
        for row in self.__board:
            print(row)

    def repr(self):
        return [[repr(tile) for tile in row] for row in self.__board]
