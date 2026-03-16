import tkinter as tk
from gui.main_window import ARPGGUI

GAME_VERSION = "0.1 Prototype"


def main():
    root = tk.Tk()
    ARPGGUI(root, GAME_VERSION)
    root.mainloop()


if __name__ == "__main__":
    main()