'''
Menu state module
'''

from enum import Enum


class State(Enum):
    '''
    Types of states
    '''
    DIFFICULTY_SELECT = 0
    GAME = 1
    LEADERBOARD_SELECT = 2
    LEADERBOARD = 3


class MenuState():
    '''
    Handles the different kind of states the window can be in
    '''
    __curr_state: State = State.DIFFICULTY_SELECT

    def get_state(self):
        '''
        Returns the current state
        '''
        return self.__curr_state

    def set_state(self, new_state: State):
        '''
        Updates the current state
        '''
        self.__curr_state = new_state
