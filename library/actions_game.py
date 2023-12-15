from library import atomics
from library.action_class import ButtonAction
from library.display import QueueItem
from library.navigation import GameMenu


class GameState:

    def __init__(self):
        self.move_direction = "right"

    def change_direction(self):
        directions = ["right", "down", "left", "up"]
        indx = directions.index(self.move_direction)
        new_indx = 0 if indx >= len(directions) - 1 else indx + 1
        self.move_direction = directions[new_indx]
        return self.move_direction


class GameActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def short_press0(self):
        GameActions.move_in_house(atomics.GAME_STATE.move_direction)

    def short_press1(self):
        atomics.GAME_STATE.change_direction()
        atomics.DISPLAY.queue_item(QueueItem("render_house"))

    def long_press1(self):
        GameActions.leave_house()
        atomics.GAME_MENU = GameMenu()
        atomics.GAME_STATE = None
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
