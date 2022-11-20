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

    def calculate_results(self):
        difficulty_score = pow(2, self.__board.get_rows())\
            * pow(2, self.__board.get_cols()) * \
            (self.__board.get_mines() /
             (self.__board.get_rows() * self.__board.get_cols()))

        time_score = self.__end_time - self.__start_time
        return (difficulty_score, time_score)

    def print(self):
        self.__board.print()

    def repr(self):
        return self.__board.repr()
