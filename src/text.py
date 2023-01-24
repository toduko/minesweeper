'''
Text module
'''

from pygame.font import Font, get_default_font

from screen import Screen


class Text:
    '''
    This class is used for a text GUI element
    '''
    __font_size: int = 20
    __x: int
    __y: int
    __text: str
    __font: Font

    def __init__(self, x: int, y: int, text: str):
        self.__x = x
        self.__y = y
        self.__text = text
        self.__font = Font(get_default_font(), self.__font_size)

    def render(self, screen: Screen):
        '''
        Renders text to the screen
        '''
        text = self.__font.render(self.__text, (0, 0, 0), (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.__x, self.__y)
        screen.get_screen().blit(text, text_rect)
