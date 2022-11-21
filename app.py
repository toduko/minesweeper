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
    __difficulty_presets = [(10, 10, 10), (16, 16, 40), (16, 30, 99)]
    __leaderboard = None

    def __init__(self):
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        pygame.display.set_icon(pygame.image.load("assets/*.png"))
        pygame.display.set_caption('Minesweeper')
        self.__font = pygame.font.Font(
            pygame.font.get_default_font(), self.__font_size)
        self.__set_screen_size(640, 480)

        while True:
            self.__render()

    def __render_button(self, y, title, on_click):
        button_width = 240
        button_height = 30
        pygame.draw.rect(self.__screen, (100, 100, 100), [
            self.__width // 2 - button_width // 2, y - button_height // 2, button_width, button_height])
        text = self.__font.render(title, (0, 0, 0), (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.__width // 2, y)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if (self.__width // 2 - button_width // 2) <= mouse_x <= (self.__width // 2 + button_width // 2)\
                and (y - button_height // 2) <= mouse_y <= (y + button_height // 2):
            if self.__lclick:
                on_click()

        self.__screen.blit(text, text_rect)

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

    def __get_top_ten_scores(self, difficulty):
        filename = "easy"
        if difficulty == 1:
            filename = "medium"
        elif difficulty == 2:
            filename = "hard"

        self.__screen.fill((0, 0, 0))

        try:
            file = open(filename, "r")

            top_ten = sorted(list(map(lambda x: float(x), filter(lambda x: x.replace(
                '.', '', 1).isdigit(), file.read().split("\n")))))[:10]

            text = self.__font.render(
                str(f"Top {filename} scores:"), (0, 0, 0), (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (self.__width // 2, 140)
            self.__screen.blit(text, text_rect)

            for i in range(len(top_ten)):
                text = self.__font.render(
                    f"{i + 1} - {top_ten[i]:0.4f} seconds", (0, 0, 0), (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = (self.__width // 2, 180 + i * 20)
                self.__screen.blit(text, text_rect)
        except FileNotFoundError:
            text = self.__font.render(
                "No scores found for this difficulty", (0, 0, 0), (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (self.__width // 2, self.__height // 2)
            self.__screen.blit(text, text_rect)

    def __render_game(self):
        state = self.__game.repr()

        pos = pygame.mouse.get_pos()
        x, y = pos[0] // self.__image_size, pos[1] // self.__image_size

        if self.__lclick:
            self.__game.show(x, y)

            if not self.__game.should_continue():
                time = self.__game.get_time()
                filename = "easy"
                if self.__difficulty == 1:
                    filename = "medium"
                elif self.__difficulty == 2:
                    filename = "hard"
                file = open(filename, "a")
                file.write(str(time) + "\n")
                file.close()

        if self.__rclick:
            self.__game.toggle_marked(x, y)

        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__last_state and self.__last_state[i][j] == state[i][j]:
                    continue
                tile = pygame.image.load(f"assets/{state[i][j]}.png")
                tile_rect = tile.get_rect()
                tile_rect.x, tile_rect.y = i * self.__image_size, j * self.__image_size
                self.__screen.blit(tile, tile_rect)

        if not self.__game.should_continue():
            text = self.__font.render(f"You won! Your time is {self.__game.get_time():0.4f}s" if self.__game.has_won(
            ) else "You lost", (0, 0, 0), (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (self.__width // 2, self.__height // 2)
            self.__screen.blit(text, text_rect)

        self.__last_state = state

    def __render_menu(self):
        def set_leaderboard(diff):
            self.__leaderboard = diff

        self.__render_button(80, "Easy", lambda: self.__start_game(0))
        self.__render_button(140, "Easy Leaderboard",
                             lambda: set_leaderboard(0))
        self.__render_button(200, "Medium", lambda: self.__start_game(1))
        self.__render_button(260, "Medium Leaderboard",
                             lambda: set_leaderboard(1))
        self.__render_button(320, "Hard", lambda: self.__start_game(2))
        self.__render_button(380, "Hard Leaderboard",
                             lambda: set_leaderboard(2))

    def __render_leaderboard(self):
        self.__get_top_ten_scores(self.__leaderboard)

    def __render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.__game = None
                    self.__last_state = None
                    self.__leaderboard = None
                    self.__set_screen_size(640, 480)

                if event.key == pygame.K_r and self.__game:
                    self.__game = Game(self.__rows, self.__cols, self.__mines)

        self.__handle_mouse()
        if self.__game:
            self.__render_game()
        elif self.__leaderboard is not None:
            self.__render_leaderboard()
        else:
            self.__render_menu()

        self.__lclick = self.__rclick = False

        pygame.display.update()

    def __set_screen_size(self, width, height):
        self.__size = self.__width, self.__height = width, height
        self.__screen = pygame.display.set_mode(self.__size)

    def __start_game(self, difficulty):
        self.__difficulty = self.__difficulty_presets[difficulty]
        self.__rows, self.__cols, self.__mines = self.__difficulty
        self.__set_screen_size(
            self.__rows * self.__image_size, self.__cols * self.__image_size)
        self.__game = Game(self.__rows, self.__cols, self.__mines)


App()
