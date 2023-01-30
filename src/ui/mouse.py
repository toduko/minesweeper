'''
Mouse module
'''

import pygame


class Mouse:
    '''
    This class is used for mouse event handling
    '''
    __CLICK_MINIMUM = 100
    __timer_lclick: int = 0
    __timer_rclick: int = 0
    __lclick: bool = False
    __rclick: bool = False

    def handle_events(self):
        '''
        Handles mouse up/down events
        '''
        left, _, right = pygame.mouse.get_pressed()

        if left:
            self.__timer_lclick += 1
        else:
            if self.__timer_lclick > self.__CLICK_MINIMUM:
                self.__lclick = True
            self.__timer_lclick = 0

        if right:
            self.__timer_rclick += 1
        else:
            if self.__timer_rclick > self.__CLICK_MINIMUM:
                self.__rclick = True
            self.__timer_rclick = 0

    def is_left_clicked(self) -> bool:
        '''
        Checks if the left mouse button is clicked
        '''
        return self.__lclick

    def is_right_clicked(self) -> bool:
        '''
        Checks if the right mouse button is clicked
        '''
        return self.__rclick

    def is_in_square(self, x_min, x_max, y_min, y_max) -> bool:
        '''
        Checks if mouse position is in a square
        '''
        x, y = self.get_pos()
        return x_min <= x <= x_max and y_min <= y <= y_max

    def get_pos(self) -> tuple[int, int]:
        '''
        Returns the mouse coordinates in the window
        '''
        return pygame.mouse.get_pos()

    def cleanup(self):
        '''
        Resets left and right clicked state to false
        '''
        self.__lclick = self.__rclick = False
