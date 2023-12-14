import display_helper
from library import atomics
from library.display import QueueItem
from library.navigation import GameMenu, MainMenu, InfoMenu


def leave_house():
    atomics.API_CLASS.leave_house()


def enter_house():
    response = atomics.API_CLASS.enter_house()
    if not response["success"]:
        return False
    queue_item = QueueItem(
        "render_house",
        data=response
    )
    atomics.DISPLAY.queue_item(queue_item)
    return True


def move_in_house(direction):
    response = atomics.API_CLASS.move(direction)
    if not response["success"]:
        return False
    queue_item = QueueItem(
        "render_house",
        data=response
    )
    atomics.DISPLAY.queue_item(queue_item)
    return True


def press0():
    if atomics.FREEZE_BUTTONS:
        print("Button 0 frozen")
        return
    if atomics.STATE == "main_menu":
        atomics.MAIN_MENU.increment_state()
    elif atomics.STATE == "game_menu":
        atomics.GAME_MENU.increment_state()
    elif atomics.STATE == "game":
        move_in_house("right")


def press1():
    if atomics.FREEZE_BUTTONS:
        print("Button 1 frozen")
        return
    if atomics.STATE == "main_menu":
        atomics.MAIN_MENU.decrement_state()
    elif atomics.STATE == "game_menu":
        atomics.GAME_MENU.decrement_state()
    elif atomics.STATE == "game":
        move_in_house("left")


def long_press0():
    if atomics.FREEZE_BUTTONS:
        return
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
    elif atomics.STATE == "game_menu":
        selected_item = atomics.GAME_MENU.selected_item
        if selected_item == "enter":
            success = enter_house()
            print(f"Enter success? {success}")
            if success:
                atomics.STATE = "game"
                atomics.GAME_MENU = None


def long_press1():
    if atomics.FREEZE_BUTTONS:
        return
    if atomics.STATE == "game_menu":
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.GAME_MENU = None
        return
    if atomics.STATE == "info_menu":
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.INFO_MENU = None
        return
    if atomics.STATE == "game":
        leave_house()
        atomics.GAME_MENU = GameMenu()
        atomics.STATE = "game_menu"


def double_press0():
    if atomics.FREEZE_BUTTONS:
        return
    if atomics.STATE == "game":
        move_in_house("up")


def double_press1():
    if atomics.FREEZE_BUTTONS:
        return
    if atomics.STATE == "game":
        move_in_house("down")
