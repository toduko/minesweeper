import sys
import pygame

from game import Game


class App:
    __image_size = 32
    __font_size = 20
    __left = False
    __right = False
    __timer_lclick = 0
    __timer_rclick = 0
    __last_state = None
    __lclick = False
    __rclick = False
    __game = None
    __difficulty_presets = {"easy": (10, 10, 10), "medium": (
        16, 16, 40), "hard": (16, 30, 99)}
    __leaderboard = None
    __leaderboard_list = False
    __button_width = 240
    __button_height = 30
    __padding = 80
    __margin = 60

    def __init__(self):
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        pygame.display.set_icon(pygame.image.load("assets/mine.png"))
        pygame.display.set_caption('Minesweeper')
        self.__font = pygame.font.Font(
            pygame.font.get_default_font(), self.__font_size)
        self.__set_menu_size()

        while True:
            self.__render()

    def __render_button(self, y, title, on_click):
        pygame.draw.rect(self.__screen, (100, 100, 100), [
            self.__width // 2 - self.__button_width // 2, y - self.__button_height // 2, self.__button_width, self.__button_height])
        self.__render_text(title.capitalize(), y)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if (self.__width // 2 - self.__button_width // 2) <= mouse_x <= (self.__width // 2 + self.__button_width // 2)\
                and (y - self.__button_height // 2) <= mouse_y <= (y + self.__button_height // 2):
            if self.__lclick:
                on_click()

    def __handle_mouse(self):
        self.__left, _, self.__right = pygame.mouse.get_pressed()

        if self.__left:
            self.__timer_lclick += 1
        else:
            if self.__timer_lclick > 100:
                self.__lclick = True
            self.__timer_lclick = 0

        if self.__right:
            self.__timer_rclick += 1
        else:
            if self.__timer_rclick > 100:
                self.__rclick = True
            self.__timer_rclick = 0

    def __render_text(self, title, y):
        text = self.__font.render(title, (0, 0, 0), (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.__width // 2, y)
        self.__screen.blit(text, text_rect)

    def __get_top_ten_scores(self):
        self.__screen.fill((0, 0, 0))

        try:
            file = open(self.__leaderboard, "r")

            top_ten = sorted(list(map(lambda x: float(x), filter(lambda x: x.replace(
                '.', '', 1).isdigit(), file.read().split("\n")))))[:10]
            if top_ten:
                self.__set_screen_size(
                    640, (len(top_ten) + 2) * (self.__margin // 2) + 2 * self.__padding)
                self.__render_text(
                    f"Top {self.__leaderboard} scores:", self.__padding)
                for i in range(len(top_ten)):
                    self.__render_text(
                        f"{i + 1} - {top_ten[i]:0.4f} seconds", self.__padding + (i + 1) * self.__margin // 2)
                self.__render_text(
                    "Press ESCAPE to go back", self.__padding + (len(top_ten) + 2) * self.__margin // 2)
            else:
                self.__render_text(
                    "No scores found for this difficulty", self.__height // 2 - self.__margin // 2)
                self.__render_text(
                    "Press ESCAPE to go back", self.__height // 2 + self.__margin // 2)
        except FileNotFoundError:
            self.__render_text(
                "No scores found for this difficulty", self.__height // 2 - self.__margin // 2)
            self.__render_text(
                "Press ESCAPE to go back", self.__height // 2 + self.__margin // 2)

    def __get_image_from_tile_char(self, char):
        if char == '#':
            return "hidden"
        elif char == 'P':
            return "flag"
        elif char == '*':
            return "mine"
        elif char == ' ':
            return "0"
        else:
            return char


    def __render_game(self):
        state = self.__game.repr()

        pos = pygame.mouse.get_pos()
        x, y = pos[0] // self.__image_size, pos[1] // self.__image_size

        if self.__lclick:
            self.__game.show(x, y)

            if not self.__game.should_continue():
                time = self.__game.get_time()
                file = open(self.__difficulty, "a")
                file.write(str(time) + "\n")
                file.close()

        if self.__rclick:
            self.__game.toggle_marked(x, y)

        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__last_state and self.__last_state[i][j] == state[i][j]:
                    continue
                tile = pygame.image.load(f"assets/{self.__get_image_from_tile_char(state[i][j])}.png")
                tile_rect = tile.get_rect()
                tile_rect.x, tile_rect.y = i * self.__image_size, j * self.__image_size
                self.__screen.blit(tile, tile_rect)

        if not self.__game.should_continue():
            self.__render_text(f"You won! Your time is {self.__game.get_time():0.4f}s" if self.__game.has_won(
            ) else "You lost", self.__height // 2)

        self.__last_state = state

    def __toggle_list(self):
        self.__leaderboard_list ^= True

    def __render_menu(self):
        for i, difficulty in enumerate(self.__difficulty_presets.keys()):
            self.__render_button(
                self.__padding + i * self.__margin, difficulty, lambda: self.__start_game(difficulty))
        self.__render_button(self.__padding + len(self.__difficulty_presets.keys())
                             * self.__margin, "leaderboards", self.__toggle_list)

    def __render_list(self):
        def set_leaderboard(difficulty):
            self.__leaderboard = difficulty

        for i, difficulty in enumerate(self.__difficulty_presets.keys()):
            self.__render_button(
                self.__padding + i * self.__margin, f"{difficulty} leaderboard", lambda: set_leaderboard(difficulty))
        self.__render_button(self.__padding + len(self.__difficulty_presets.keys())
                             * self.__margin, "back", self.__toggle_list)

    def __get_menu(self):
        self.__game = None
        self.__last_state = None
        self.__leaderboard = None
        self.__set_menu_size()

    def __render_leaderboard(self):
        self.__get_top_ten_scores()

    def __set_menu_size(self):
        self.__set_screen_size(
            640, self.__padding * 2 + (len(self.__difficulty_presets.keys()) + 1) * self.__margin)

    def __render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.__get_menu()

                if event.key == pygame.K_r and self.__game:
                    self.__game = Game(self.__rows, self.__cols, self.__mines)

        self.__handle_mouse()
        if self.__game:
            self.__render_game()
        elif self.__leaderboard is not None:
            self.__render_leaderboard()
        elif self.__leaderboard_list:
            self.__render_list()
        else:
            self.__render_menu()

        self.__lclick = self.__rclick = False

        pygame.display.update()

    def __set_screen_size(self, width, height):
        self.__size = self.__width, self.__height = width, height
        self.__screen = pygame.display.set_mode(self.__size)

    def __start_game(self, difficulty):
        self.__difficulty = difficulty
        self.__rows, self.__cols, self.__mines = self.__difficulty_presets[self.__difficulty]
        self.__set_screen_size(
            self.__rows * self.__image_size, self.__cols * self.__image_size)
        self.__game = Game(self.__rows, self.__cols, self.__mines)


App()
