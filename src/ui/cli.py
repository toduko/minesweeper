'''
CLI module
'''


from src.base.game import Game
from src.base.board import Board


class CLI:
    '''
    This class is used to play minesweeper on the console.
    It provides an interface for playing using commands.
    '''

    def __init__(self):
        self.__accept_input: bool = True
        self.__game: Game = None

        while self.__accept_input:
            cmd: str = input("Minesweeper CLI> ")
            self.__parse(cmd)

        print("Thank you for playing!")

    def __parse(self, cmd: str):
        '''
        Parses the command
        '''
        instr: str
        args: list[str]
        instr, *args = cmd.split(' ')

        def should_accept_cmd(expected_num_args: int = 2) -> bool:
            if instr.lower() == "new" and \
                    not Board.is_valid_board(int(args[0]),
                                             int(args[1]),
                                             int(args[2])):
                print("Not a valid game")
                return False

            if self.__game is None and instr.lower() in ("show", "toggle"):
                print("Not in an active game")
                return False

            if len(args) != expected_num_args or args == filter(lambda arg: arg.isalphanum(), args):
                print("Invalid arguments")
                return False

            return True

        if instr.lower() == "help":
            print("Here are the list of commands:")
            print("help - prints this menu")
            print("exit - exits the cli")
            print("new - starts new game. Usage new <rows> <cols> <mines>")
            print("show - shows board at specific coordinates. Usage show <x> <y>")
            print(
                "toggle - toggles board flag at specific coordinates. Usage toggle <x> <y>")
        elif instr.lower() == "exit":
            self.__accept_input = False
        elif instr.lower() == "new":
            if not should_accept_cmd(3):
                return

            print(
                f"Starting a new game with {args[0]} rows, {args[1]} columns and {args[2]} mines")
            self.__game = Game((int(args[0]), int(args[1]), int(args[2])))
            self.__game.print()
        elif instr.lower() == "show":
            if not should_accept_cmd():
                return

            self.__game.show(int(args[0]), int(args[1]))
            self.__game.print()

            if not self.__game.should_continue():
                time = self.__game.get_time()
                if self.__game.has_won():
                    print("You won!")
                    print(f"{time = }")
                else:
                    print("You lost!")

                self.__game = None
        elif instr.lower() == "toggle":
            if not should_accept_cmd():
                return

            self.__game.toggle_marked(int(args[0]), int(args[1]))
            self.__game.print()
        else:
            print("Invalid command. Type help to see a list of available commands.")
