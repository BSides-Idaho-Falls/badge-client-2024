from library import atomics
from library.action_class import ButtonAction
from library.navigation import MainMenu


class LightMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def action_forward(self):
        atomics.ANIMATE_MENU.increment_state()

    def action_backward(self):
        atomics.ANIMATE_MENU.decrement_state()

    def primary_select(self):
        selected_item: str = atomics.LIGHT_MENU.selected_item
        if selected_item == "off":
            atomics.LIGHTS.off()
            return
        atomics.LIGHTS.on()

    def secondary_select(self):
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.LIGHT_MENU = None

