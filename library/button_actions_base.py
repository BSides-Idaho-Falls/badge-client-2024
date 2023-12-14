import display_helper
from library import atomics
from library.display import QueueItem
from library.navigation import GameMenu, MainMenu, InfoMenu


def press0():
    if atomics.FREEZE_BUTTONS:
        print("Button 0 frozen")
        return
    print("Pressed 0")
    if atomics.STATE == "main_menu":
        atomics.MAIN_MENU.increment_state()
    elif atomics.STATE == "game_menu":
        atomics.GAME_MENU.increment_state()


def press1():
    if atomics.FREEZE_BUTTONS:
        print("Button 1 frozen")
        return
    print("Pressed 1")
    if atomics.STATE == "main_menu":
        atomics.MAIN_MENU.decrement_state()
    elif atomics.STATE == "game_menu":
        atomics.GAME_MENU.decrement_state()


def long_press0():
    if atomics.FREEZE_BUTTONS:
        return
    print("Long pressed 0")
    if atomics.STATE == "main_menu":
        selected_item = atomics.MAIN_MENU.selected_item
        if selected_item == "game":
            atomics.GAME_MENU = GameMenu()
            atomics.STATE = "game_menu"
            atomics.MAIN_MENU = None
        elif selected_item == "info":
            atomics.STATE = "info_menu"
            atomics.MAIN_MENU = None
            lines = [
                atomics.NETWORK_SSID,
                atomics.NETWORK_MAC,
                atomics.NETWORK_IP
            ]
            atomics.INFO_MENU = atomics.INFO_MENU = InfoMenu(lines)
        elif selected_item == "potato":
            for i in range(0, 3):
                atomics.DISPLAY.queue_item(
                    QueueItem(
                        "animation",
                        data=display_helper.WINKING_POTATO,
                        ms_between_frames=50
                    )
                )
            atomics.MAIN_MENU.modified = True


def long_press1():
    if atomics.FREEZE_BUTTONS:
        return
    print("Long pressed 1")
    if atomics.STATE == "game_menu":
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.GAME_MENU = None
    if atomics.STATE == "info_menu":
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.INFO_MENU = None


def double_press0():
    if atomics.FREEZE_BUTTONS:
        return
    print("Double pressed 0")


def double_press1():
    if atomics.FREEZE_BUTTONS:
        return
    print("Double pressed 1")
