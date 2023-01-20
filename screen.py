'''
Screen module
'''

from pygame import Surface
from pygame.display import set_mode


class Screen:
    __screen: Surface
    __width: int
    __height: int

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
