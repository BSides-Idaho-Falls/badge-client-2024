from library import atomics
from library.action_class import ButtonAction
from library.navigation import GameMenu


class ShopMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def action_forward(self):
        atomics.SHOP_MENU.increment_state()

    def action_backward(self):
        atomics.SHOP_MENU.decrement_state()

    def secondary_select(self):
        atomics.GAME_MENU = GameMenu()
        atomics.STATE = "game_menu"
        atomics.SHOP_MENU = None

    def primary_select(self):
        selected_item = atomics.SHOP_MENU.selected_item
        if selected_item == "buy":
            atomics.API_CLASS.shop_buy_wall()
        elif selected_item == "sell":
            atomics.API_CLASS.shop_sell_wall()
        atomics.SHOP_MENU.modified = True
