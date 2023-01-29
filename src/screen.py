'''
Screen module
'''

from pygame import Surface
from pygame.display import set_mode


class Screen:
    '''
    This class is used to managy the screen
    '''
    __screen: Surface
    __width: int
    __height: int
    __padding: int = 80
    __margin: int = 60
    __default_width = 640

    def set_size(self, width: int, height: int):
        '''
        Sets screen size
        '''
        size = self.__width, self.__height = width, height
        self.__screen = set_mode(size)

    def get_screen(self) -> Surface:
        '''
        Returns the screen surface
        '''
        return self.__screen

    def get_width(self) -> int:
        '''
        Returns screen width
        '''
        return self.__width

    def get_height(self) -> int:
        '''
        Returns screen height
        '''
        return self.__height

    def get_margin(self) -> int:
        '''
        Returns margin between items on screen
        '''
        return self.__margin

    def get_padding(self) -> int:
        '''
        Returns padding of items on screen
        '''
        return self.__padding

    def set_menu_size(self, items_amount: int):
        '''
        Sets the size of the menu depending on the amount of items in it
        '''
        self.set_size(self.__default_width,
                      self.__padding * 2 + items_amount * self.__margin)
