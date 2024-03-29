'''
Tile module
'''

from __future__ import annotations


class Tile:
    '''
    This class represents a single tile.
    It can be either a mine or not.
    It can be hidden or shown.
    Also information on neighbouring mines can be stored.
    '''

    def __init__(self, is_mine: bool):
        self.__is_mine: bool = is_mine
        self.__hidden: bool = True
        self.__marked: bool = False

    @staticmethod
    def repr(tile: Tile, neighbouring_mines):
        '''
        Returns the char representation of a tile
        '''
        if not tile:
            return '#'
        if tile.is_marked():
            return 'P'
        if tile.is_hidden():
            return '#'
        if tile.is_mine():
            return '*'

        return ' ' if not neighbouring_mines else str(neighbouring_mines)

    def is_hidden(self) -> bool:
        '''
        Checks if a tile is hidden
        '''
        return self.__hidden

    def show(self):
        '''
        Shows unmarked tile
        '''
        if not self.__marked:
            self.__hidden = False

    def is_marked(self) -> bool:
        '''
        Checks if a tile is marked
        '''
        return self.__marked

    def toggle_marked(self):
        '''
        Toggles the tile marked state if it is hidden
        '''
        if self.__hidden:
            self.__marked ^= True

    def is_mine(self) -> bool:
        '''
        Checks if the tile is a mine
        '''
        return self.__is_mine
