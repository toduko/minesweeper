'''
Game tests
'''

from time import perf_counter
from random import randint
from src.base.game import Game
from src.base.tile import Tile
from src.base.board import Board

ROWS: int = 50
COLS: int = 50
NUM_MINES: int = 300
tiles: list[list[Tile]] = [[Tile((row, col)
                                 in Board.generate_mine_coords(ROWS,
                                                               COLS,
                                                               NUM_MINES, set()))
                            for col in range(COLS)]
                           for row in range(ROWS)]


def test_winning_a_game():
    '''
    Tests winning a game
    '''
    game = Game(tiles)

    for x in range(ROWS):
        for y in range(COLS):
            if not tiles[x][y].is_mine():
                game.show(x, y)

    assert not game.should_continue() and game.has_won()


def test_losing_a_game():
    '''
    Tests losing a game
    '''
    game = Game(tiles)

    for x in range(ROWS):
        for y in range(COLS):
            if tiles[x][y].is_mine():
                game.show(x, y)
                break

    assert not game.should_continue() and game.has_lost()


def test_timer():
    '''
    Tests if game is being timed properly
    '''
    epsilon = 0.1
    start = perf_counter()
    game = Game(tiles)

    while game.should_continue():
        game.show(randint(0, ROWS - 1), randint(0, COLS - 1))

    end = perf_counter()

    assert abs(game.get_time() - (end - start)) < epsilon
