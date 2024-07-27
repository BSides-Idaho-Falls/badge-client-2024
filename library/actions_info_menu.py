from library import atomics
from library.action_class import ButtonAction
from library.navigation import MainMenu, OfflineMenu


class InfoMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def secondary_select(self):
        atomics.MAIN_MENU = MainMenu()
        atomics.OFFLINE_MENU = OfflineMenu()
        atomics.STATE = "main_menu"
        atomics.INFO_MENU = None

