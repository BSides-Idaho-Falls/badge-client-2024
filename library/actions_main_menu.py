import display_helper
from library import atomics
from library.action_class import ButtonAction
from library.display import QueueItem
from library.navigation import InfoMenu, GameMenu, AnimationMenu


class MainMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def action_forward(self):
        atomics.MAIN_MENU.increment_state()

    def action_backward(self):
        atomics.MAIN_MENU.decrement_state()

    def primary_select(self):
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
            atomics.INFO_MENU = InfoMenu(lines)
        elif selected_item == "animate":
            atomics.ANIMATE_MENU = AnimationMenu()
            atomics.STATE = "animate_menu"
            atomics.MAIN_MENU = None
        elif selected_item == "test":
            atomics.DISPLAY.queue_item(QueueItem(
                "popup",
                {"message": "test", "delay": 100}
            ))
