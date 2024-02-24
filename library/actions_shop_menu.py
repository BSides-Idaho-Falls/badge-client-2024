from library import atomics
from library.action_class import ButtonAction
from library.navigation import GameMenu


class ShopMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def short_press0(self):
        atomics.SHOP_MENU.increment_state()

    def short_press1(self):
        atomics.SHOP_MENU.decrement_state()

    def long_press1(self):
        atomics.GAME_MENU = GameMenu()
        atomics.STATE = "game_menu"
        atomics.SHOP_MENU = None

    def long_press0(self):
        selected_item = atomics.SHOP_MENU.selected_item
        if selected_item == "buy":
            atomics.API_CLASS.shop_buy_wall()
        elif selected_item == "sell":
            atomics.API_CLASS.shop_sell_wall()
