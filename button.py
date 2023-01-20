'''
Button module
'''

from typing import Callable
from pygame.draw import rect

from screen import Screen
from mouse import Mouse
from text import Text


class Button:
    '''
    This class is used for a button GUI element
    '''
    __x: int
    __y: int
    __width: int
    __height: int
    __text: Text
    __on_click: Callable[[], None]

    def __init__(self, x: int, y: int, text: str, on_click: Callable[[], None], width: int = 240, height: int = 30):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__text = Text(self.__x, self.__y, text.capitalize())
        self.__on_click = on_click

    def render(self, screen: Screen, mouse: Mouse):
        '''
        Renders button to the screen
        '''
        rect(screen.get_screen(), (100, 100, 100), [
            self.__x - self.__width // 2,
            self.__y - self.__height // 2,
            self.__width,
            self.__height])
        self.__text.render(screen)
        if (mouse.is_in_square(self.__x - self.__width // 2,
                               self.__x + self.__width // 2,
                               self.__y - self.__height // 2,
                               self.__y + self.__height // 2)) \
                and mouse.is_left_clicked():
            self.__on_click()
