from library import atomics
from library.action_class import ButtonAction
from library.navigation import InfoMenu, AnimationMenu


class OfflineMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def short_press0(self):
        atomics.OFFLINE_MENU.increment_state()

    def short_press1(self):
        atomics.OFFLINE_MENU.decrement_state()

    def long_press0(self):
        selected_item = atomics.OFFLINE_MENU.selected_item
        if selected_item == "info":
            atomics.STATE = "info_menu"
            atomics.OFFLINE_MENU = None
            atomics.MAIN_MENU = None
            lines = [
                atomics.NETWORK_SSID,
                atomics.NETWORK_MAC,
                atomics.NETWORK_IP
            ]
            atomics.INFO_MENU = atomics.INFO_MENU = InfoMenu(lines)
        elif selected_item == "animate":
            atomics.ANIMATE_MENU = AnimationMenu()
            atomics.STATE = "animate_menu"
            atomics.OFFLINE_MENU = None
            atomics.MAIN_MENU = None
