from time import perf_counter
from board import Board


class Game:
    def __init__(self, rows, cols, num_mines):
        self.__board = Board(rows, cols, num_mines)
        self.__start_time = perf_counter()
        self.__end_time = perf_counter()

    def show(self, x, y):
        if self.should_continue():
            if not self.__board.has_started():
                self.__start_time = perf_counter()

            self.__board.show(x, y)

            if not self.__board.should_continue():
                self.__end_time = perf_counter()

    def toggle_marked(self, x, y):
        if self.should_continue():
            self.__board.toggle_marked(x, y)

    def should_continue(self):
        return self.__board.should_continue()

    def has_won(self):
        return self.__board.has_won()

    def get_time(self):
        return self.__end_time - self.__start_time

    def print(self):
        self.__board.print()

    def repr(self):
        return self.__board.repr()
