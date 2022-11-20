class Tile:
    def __init__(self):
        self.__mine = False
        self.__hidden = True
        self.__marked = False
        self.__neighbour_mines = 0

    def is_hidden(self):
        return self.__hidden

    def show(self):
        if not self.__hidden:
            print("Tile already shown")

        if not self.__marked:
            self.__hidden = False
        else:
            print("Cannot show marked tiles")

    def is_marked(self):
        return self.__marked

    def toggle_marked(self):
        if self.__hidden:
            self.__marked ^= True
        else:
            print("Cannot mark shown tiles")

    def set_mine(self):
        self.__mine = True

    def is_mine(self):
        return self.__mine

    def get_neighbour_mines(self):
        return self.__neighbour_mines

    def set_neighbour_mines(self, amount):
        self.__neighbour_mines = amount

    def __repr__(self):
        if self.__marked:
            return 'P'
        if self.__hidden:
            return '#'
        if self.__mine:
            return '*'
        return ' ' if self.__neighbour_mines == 0 else str(self.__neighbour_mines)
