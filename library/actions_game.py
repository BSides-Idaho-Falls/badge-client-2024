from library import atomics
from library.action_class import ButtonAction
from library.display import QueueItem
from library.navigation import GameMenu


class GameActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def short_press0(self):
        GameActions.move_in_house("right")

    def short_press1(self):
        GameActions.move_in_house("left")

    def double_press0(self):
        GameActions.move_in_house("up")

    def double_press1(self):
        GameActions.move_in_house("down")

    def long_press1(self):
        GameActions.leave_house()
        atomics.GAME_MENU = GameMenu()
        atomics.STATE = "game_menu"

    @staticmethod
    def leave_house():
        atomics.API_CLASS.leave_house()

    @staticmethod
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
