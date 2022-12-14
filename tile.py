'''
Tile module
'''


class Tile:
    '''
    This class represents a single tile.
    It can be either a mine or not.
    It can be hidden or shown.
    Also information on neighbouring mines can be stored.
    '''

    def __init__(self):
        self.__mine: bool = False
        self.__hidden: bool = True
        self.__marked: bool = False
        self.__neighbour_mines: int = 0

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

    def set_mine(self):
        '''
        Sets the tile to a mine
        '''
        self.__mine = True

    def is_mine(self) -> bool:
        '''
        Checks if the tile is a mine
        '''
        return self.__mine

    def get_neighbour_mines(self) -> int:
        '''
        Returns the amount of neighbouring mines
        '''
        return self.__neighbour_mines

    def set_neighbour_mines(self, amount: int):
        '''
        Sets the amount of neighbouring mines
        '''
        self.__neighbour_mines = amount

    def __repr__(self) -> str:
        if self.__marked:
            return 'P'
        if self.__hidden:
            return '#'
        if self.__mine:
            return '*'
        return ' ' if self.__neighbour_mines == 0 else str(self.__neighbour_mines)
