from library import atomics
from library.action_class import ButtonAction
from library.display import QueueItem
from library.light_handler import LightPatterns
from library.navigation import GameMenu


class GameState:

    def __init__(self):
        self.move_direction = "right"
        self.current_location = [0, 15]
        self.build_action = "build"  # build, clear, vault
        self.own_house: bool = False

    def switch_build_action(self):
        actions = ["build", "clear", "vault"]
        indx = actions.index(self.build_action)
        new_indx = 0 if indx >= len(actions) - 1 else indx + 1
        self.build_action = actions[new_indx]
        return self.build_action

    def change_direction(self, direction=None):
        directions = ["right", "down", "left", "up"]
        if direction and direction in directions:
            self.move_direction = direction
            return self.move_direction
        indx = directions.index(self.move_direction)
        new_indx = 0 if indx >= len(directions) - 1 else indx + 1
        self.move_direction = directions[new_indx]
        return self.move_direction

    def looking_at(self):
        if self.move_direction == "left":
            return [self.current_location[0] - 1, self.current_location[1]]
        if self.move_direction == "right":
            return [self.current_location[0] + 1, self.current_location[1]]
        if self.move_direction == "up":
            return [self.current_location[0], self.current_location[1] + 1]
        if self.move_direction == "down":
            return [self.current_location[0], self.current_location[1] - 1]
        return None


class GameActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def hybrid_action_move(self, direction: str):
        atomics.GAME_STATE.change_direction(direction=direction)
        atomics.DISPLAY.queue_item(QueueItem("render_house"))
        self.action_forward()

    def action_forward(self):
        GameActions.move_in_house(atomics.GAME_STATE.move_direction)

    def action_backward(self):
        atomics.GAME_STATE.change_direction()
        atomics.DISPLAY.queue_item(QueueItem("render_house"))

    def secondary_select(self):
        GameActions.leave_house()

    def primary_select(self):
        if not atomics.GAME_STATE.own_house:
            return
        looking_at = atomics.GAME_STATE.looking_at()
        build_action = atomics.GAME_STATE.build_action  # build, clear, vault
        x: int = looking_at[0]
        y: int = looking_at[1]
        print(f"Looking at: {x}, {y}")
        response = {"success": False}
        if build_action == "vault":
            response = atomics.API_CLASS.move_vault(x, y)
        if build_action == "build":
            response = atomics.API_CLASS.place_wall(x, y)
        if build_action == "clear":
            response = atomics.API_CLASS.clear_wall(x, y)
        if response["success"]:
            queue_item = QueueItem(
                "render_house",
                data=response
            )
            atomics.DISPLAY.queue_item(queue_item)
            player_location: list = response["player_location"] if "player_location" in response else []
            x, y = player_location[0], player_location[1]
            atomics.GAME_STATE.current_location = [x, y]
        else:
            atomics.DISPLAY.queue_item(QueueItem("popup", {
                "delay": 2100,
                "message": [
                    "Can't edit",
                    "selection"
                ]
            }))
            atomics.LIGHTS.adaptive_queue(LightPatterns.get_pattern("blink_red"))

    def primary_modify(self):
        if not atomics.GAME_STATE.own_house:
            return
        build_action = atomics.GAME_STATE.switch_build_action()
        print(f"Switched mode to: {build_action}")
        atomics.DISPLAY.queue_item(QueueItem("render_house"))

    @staticmethod
    def leave_house():
        atomics.API_CLASS.leave_house()
        atomics.GAME_MENU = GameMenu()
        atomics.GAME_STATE = None
        atomics.STATE = "game_menu"

    @staticmethod
    def move_in_house(direction):
        response = atomics.API_CLASS.move(direction)
        print(response)
        if not response["success"]:
            message = response.get("reason", "")
            if message == "You are not in a house.":
                print("You are no longer in a house! You have been kicked out.")
                atomics.GAME_MENU = GameMenu()
                atomics.GAME_STATE = None
                atomics.STATE = "game_menu"
                atomics.LIGHTS.adaptive_queue(LightPatterns.get_pattern("blink_red"))
            return False

        if "robbed" in response and response["robbed"]:
            dollars: int = response["contents"]["dollars"]
            print(f"You robbed the house! You got {dollars} dollars.")
            for item in LightPatterns.get_pattern("rob_success"):
                atomics.LIGHTS.adaptive_queue(item)
            atomics.DISPLAY.queue_item(QueueItem("popup", {
                "delay": 2100,
                "message": [
                    "Success!",
                    f"Won ${dollars}"
                ]
            }))
            # House robbed successfully!
            GameActions.leave_house()
            return True
        queue_item = QueueItem(
            "render_house",
            data=response
        )
        atomics.DISPLAY.queue_item(queue_item)
        player_location = response["player_location"]
        x, y = player_location[0], player_location[1]
        atomics.GAME_STATE.current_location = [x, y]
        if x == 0 and y == 15:  # Walking back through the door :)
            GameActions.leave_house()
        return True
