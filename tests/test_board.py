'''
Board tests
'''
from random import randint
from src.base.board import Board
from src.base.tile import Tile

ROWS: int = 50
COLS: int = 50
NUM_MINES: int = 300
NUM_FORBIDDEN: int = 100
forbidden: set[tuple[int]] = set()

while len(forbidden) < NUM_FORBIDDEN:
    forbidden.add((randint(0, ROWS - 1), randint(0, COLS - 1)))


def test_mine_coords_generation():
    '''
    Tests the generation of mine coordinates
    '''
    mine_coords: tuple[int, int] = Board.generate_mine_coords(
        ROWS, COLS, NUM_MINES, forbidden)

    for x, y in mine_coords:
        assert (x, y) not in forbidden

    board: Board = Board([[Tile((x, y) in mine_coords)
                          for y in range(COLS)] for x in range(ROWS)])

    for x, y in forbidden:
        board.show(x, y)
        assert board.should_continue()


def test_board_validity_check():
    '''
    Tests the board validation
    '''
    assert not Board.is_valid_board(10, 10, 0)
    assert not Board.is_valid_board(10, 10, 91)
    assert not Board.is_valid_board(100, 100, 999)
    assert not Board.is_valid_board(100, 100, 99001)
    assert Board.is_valid_board(10, 10, 10)
    assert Board.is_valid_board(100, 100, 1000)
