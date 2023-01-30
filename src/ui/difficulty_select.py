'''
DifficultySelect module
'''

from functools import partial
from typing import Callable

from src.ui.menu_state import MenuState, State
from src.ui.screen import Screen
from src.ui.button import Button
from src.ui.mouse import Mouse


class DifficultySelect:
    '''
    This class is used for the rendering of difficulty select menu
    '''

    def render(self,
               screen: Screen,
               mouse: Mouse,
               state: MenuState,
               difficulty_presets: dict[str, tuple[int, int, int]],
               start_game: Callable):
        '''
        Renders difficulty select menu to the screen
        '''
        for i, difficulty in enumerate(difficulty_presets.keys()):
            Button(screen.get_width() // 2,
                   screen.get_padding() + i * screen.get_margin(),
                   difficulty,
                   partial(start_game,
                           screen,
                           state,
                           difficulty_presets[difficulty],
                           difficulty)).render(screen, mouse)
        Button(screen.get_width() // 2,
               screen.get_padding() +
               len(difficulty_presets.keys()) *
               screen.get_margin(),
               "leaderboards",
               lambda: state.set_state(State.LEADERBOARD_SELECT)).render(screen, mouse)
