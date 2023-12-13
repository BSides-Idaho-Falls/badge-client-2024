from library import atomics
from library.navigation import GameMenu, MainMenu


def press0():
    print("Pressed 0")
    if atomics.STATE == "main_menu":
        atomics.MAIN_MENU.increment_state()
    elif atomics.STATE == "game_menu":
        atomics.GAME_MENU.increment_state()


def press1():
    print("Pressed 1")
    if atomics.STATE == "main_menu":
        atomics.MAIN_MENU.decrement_state()
    elif atomics.STATE == "game_menu":
        atomics.GAME_MENU.decrement_state()


def long_press0():
    print("Long pressed 0")
    if atomics.STATE == "main_menu":
        selected_item = atomics.MAIN_MENU.selected_item
        if selected_item == "game":
            atomics.GAME_MENU = GameMenu()
            atomics.STATE = "game_menu"
            atomics.MAIN_MENU = None


def long_press1():
    print("Long pressed 1")
    if atomics.STATE == "game_menu":
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.GAME_MENU = None


def double_press0():
    print("Double pressed 0")


def double_press1():
    print("Double pressed 1")
