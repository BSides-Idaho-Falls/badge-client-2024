import display_helper
from library import atomics
from library.action_class import ButtonAction
from library.display import QueueItem
from library.navigation import InfoMenu, GameMenu


class MainMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def short_press0(self):
        atomics.MAIN_MENU.increment_state()

    def short_press1(self):
        atomics.MAIN_MENU.decrement_state()

    def long_press0(self):
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
