'''
Minesweeper module
'''

import sys

from gui import GUI
from cli import CLI

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) > 1:
        raise Exception("Too much arguments")

    USE_GUI: bool

    if not args:
        USE_GUI = True
    else:
        if args[0].lower() == "gui":
            USE_GUI = True
        elif args[0].lower() == "cli":
            USE_GUI = False
        else:
            raise Exception("Invalid arguments")

    if USE_GUI:
        GUI()
    else:
        CLI()
