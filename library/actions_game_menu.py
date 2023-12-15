from library import atomics
from library.action_class import ButtonAction
from library.display import QueueItem
from library.navigation import MainMenu


class GameMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def short_press0(self):
        atomics.GAME_MENU.increment_state()

    def short_press1(self):
        atomics.GAME_MENU.decrement_state()

    def long_press1(self):
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.GAME_MENU = None

    def long_press0(self):
        selected_item = atomics.GAME_MENU.selected_item
        if selected_item == "enter":
            success = GameMenuActions.enter_house()
            print(f"Enter success? {success}")
            if success:
                atomics.STATE = "game"
                atomics.GAME_MENU = None

    @staticmethod
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
