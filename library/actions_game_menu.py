from library import atomics
from library.action_class import ButtonAction
from library.actions_game import GameState
from library.display import QueueItem
from library.navigation import MainMenu, ShopMenu


class GameMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def action_forward(self):
        atomics.GAME_MENU.increment_state()

    def action_backward(self):
        atomics.GAME_MENU.decrement_state()

    def secondary_select(self):
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.GAME_MENU = None

    def primary_select(self):
        selected_item = atomics.GAME_MENU.selected_item
        if selected_item == "enter":
            success = GameMenuActions.enter_house()
            print(f"Enter success? {success}")
            if success:
                atomics.STATE = "game"
                atomics.GAME_MENU = None
                atomics.GAME_STATE = GameState()
                atomics.GAME_STATE.own_house = True
        elif selected_item == "rob":
            success = GameMenuActions.rob_house()
            if success:
                atomics.STATE = "game"
                atomics.GAME_MENU = None
                atomics.GAME_STATE = GameState()
                atomics.GAME_STATE.own_house = False
        elif selected_item == "shop":
            atomics.STATE = "shop_menu"
            atomics.GAME_MENU = None
            atomics.SHOP_MENU = ShopMenu()
            vault_contents: dict = atomics.API_CLASS.inquire_vault().get("vault", {})
            atomics.SHOP_MENU.dollars = vault_contents["dollars"]
            atomics.SHOP_MENU.walls = vault_contents["walls"]
            atomics.SHOP_MENU.update_header()

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

    @staticmethod
    def rob_house():
        response = atomics.API_CLASS.rob_house()
        if not response or not response["success"]:
            atomics.DISPLAY.queue_item(QueueItem("popup", {
                "delay": 50,
                "message": [
                    "No houses", "to rob"
                ]
            }))
            print(f"There are no houses available to rob!")
            return False
        queue_item = QueueItem(
            "render_house",
            data=response
        )
        atomics.DISPLAY.queue_item(queue_item)
        return True
