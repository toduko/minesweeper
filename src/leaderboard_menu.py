'''
Leaderboard menu module
'''

from functools import partial

from src.utils import get_top_k_scores
from src.menu_state import MenuState, State
from src.screen import Screen
from src.button import Button
from src.mouse import Mouse
from src.text import Text


class LeaderboardMenu:
    '''
    This class is used for the rendering of the leaderboard and the selection of it
    '''
    __difficulty: str = ""
    __top_scores_amount = 10

    def __render_leaderboard_list(self,
                                  screen: Screen,
                                  mouse: Mouse,
                                  state: MenuState,
                                  difficulty_presets: dict[str, tuple[int, int, int]]):
        '''
        Renders the leaderboard depending on the presets
        '''
        def set_leaderboard(difficulty: str):
            self.__difficulty = difficulty
            state.set_state(State.LEADERBOARD)

        for i, difficulty in enumerate(difficulty_presets.keys()):
            Button(screen.get_width() // 2,
                   screen.get_padding() + i * screen.get_margin(),
                   f"{difficulty} leaderboard",
                   partial(set_leaderboard, difficulty)).render(screen, mouse)
        Button(screen.get_width() // 2,
               screen.get_padding() +
               len(difficulty_presets.keys()) * screen.get_margin(),
               "back",
               lambda: state.set_state(State.DIFFICULTY_SELECT)).render(screen, mouse)

    def __render_leaderboard(self, screen: Screen):
        '''
        Renders a list depending on the difficulty
        '''
        screen.get_screen().fill((0, 0, 0))

        try:
            top_scores = get_top_k_scores(self.__top_scores_amount,
                                          self.__difficulty)

            if not top_scores:
                raise LookupError

            screen.set_size(
                640, (len(top_scores) + 2) * (screen.get_margin() // 2) + 2 * screen.get_padding())
            Text(screen.get_width() // 2,
                 screen.get_padding(), f"Top {self.__difficulty} scores:").render(screen)
            for i, score in enumerate(top_scores):
                Text(screen.get_width() // 2,
                     screen.get_padding() + (i + 1) * screen.get_margin() // 2,
                     f"{i + 1} - {score:0.4f} seconds").render(screen)
            Text(screen.get_width() // 2,
                 screen.get_padding() + (len(top_scores) + 2) * screen.get_margin() // 2,
                 "Press ESCAPE to go back").render(screen)
        except (FileNotFoundError, LookupError):
            Text(screen.get_width() // 2,
                 screen.get_height() // 2 - screen.get_margin() // 2,
                 "No scores found for this difficulty").render(screen)
            Text(screen.get_width() // 2,
                 screen.get_height() // 2 + screen.get_margin() // 2,
                 "Press ESCAPE to go back").render(screen)

    def render(self,
               screen: Screen,
               mouse: Mouse,
               state: MenuState,
               difficulty_presets: dict[str, tuple[int, int, int]]):
        '''
        Decides whether to render a leaderboard or a list of leaderboards
        depending on the state
        '''
        if state.get_state() == State.LEADERBOARD_SELECT:
            self.__render_leaderboard_list(
                screen, mouse, state, difficulty_presets)
        else:
            self.__render_leaderboard(screen)
