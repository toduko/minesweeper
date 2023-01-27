lint:
    @python -m pylint src

test:
    @python -m pytest -s

gui:
    @python -m src.minesweeper gui

cli:
    @python -m src.minesweeper cli