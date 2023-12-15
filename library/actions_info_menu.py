from library import atomics
from library.action_class import ButtonAction
from library.navigation import MainMenu


class InfoMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def long_press1(self):
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.INFO_MENU = None

