from gui import GUI
from cli import CLI

if __name__ == '__main__':
    use_gui = True

    if use_gui:
        GUI()
    else:
        CLI()
