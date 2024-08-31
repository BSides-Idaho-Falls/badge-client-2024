from display_helper import ANIMATION_MAPPER
from library import atomics


class Menu:

    def __init__(self):
        self.header = None
        self.menu_name = "Abstract"
        self.selected_item: str = "nop"
        self.menu_order = []
        self.modified = True
        self.actions = {"nop": "NOP"}

    def increment_state(self):
        if "next" not in self.actions[self.selected_item]:
            indx = self.menu_order.index(self.selected_item)
            new_indx = 0 if indx >= len(self.menu_order) - 1 else indx + 1
            self.selected_item = self.menu_order[new_indx]
            self.modified = True
            return self.selected_item
        self.selected_item = self.actions[self.selected_item]["next"]
        self.modified = True
        return self.selected_item

    def decrement_state(self):
        if "before" not in self.actions[self.selected_item]:
            indx = self.menu_order.index(self.selected_item)
            new_indx = len(self.menu_order) - 1 if indx == 0 else indx - 1
            self.selected_item = self.menu_order[new_indx]
            self.modified = True
            return self.selected_item
        self.selected_item = self.actions[self.selected_item]["before"]
        self.modified = True
        return self.selected_item

    def build_menu(self, show_selector=True, refresh=False):
        lines = [] if not self.header else [self.header]
        for k in self.menu_order:
            item = self.actions[k]
            if isinstance(item, str):
                message = f"{'>' if k == self.selected_item else ' '} {item}"
                lines.append(message)
                continue
            if "hidden" in item and item["hidden"]:
                continue
            message = f"{'>' if k == self.selected_item and show_selector else ' '} {item['message']}"
            lines.append(message)
        final_lines = []
        max_lines = 4 if self.header else 5
        if len(lines) > max_lines:
            found_selected = False
            for line in lines:
                if line.startswith(">"):
                    found_selected = True
                    final_lines.append(line)
                elif found_selected:
                    if len(final_lines) < max_lines:
                        final_lines.append(line)
        else:
            final_lines = lines
        return final_lines


class MainMenu(Menu):

    def __init__(self):
        super().__init__()
        self.menu_name = "main_menu"
        self.header = "-- Main Menu --"
        self.selected_item: str = "info"
        self.menu_order = [
            "info", "game", "lights", "animate"
        ]
        self.actions = {
            "info": "Info",
            "game": "Game",
            "lights": "Lights",
            "animate": "Animations"
        }


class OfflineMenu(Menu):

    def __init__(self):
        super().__init__()
        self.menu_name = "offline_menu"
        self.header = "-- Offline --"
        self.selected_item: str = "info"
        self.menu_order = [
            "info", "lights", "animate"
        ]
        self.actions = {
            "info": "Info",
            "lights": "Lights",
            "animate": "Animations"
        }


class ShopMenu(Menu):

    def __init__(self):
        super().__init__()
        self.menu_name = "shop_menu"
        self.header = "$? | ?"
        self.selected_item: str = "buy"
        self.menu_order = [
            "buy", "sell"
        ]
        self.actions = {
            "buy": "Buy Wall",
            "sell": "Sell Wall"
        }
        self.dollars = 0
        self.walls = 0

    def update_header(self):
        self.header = f"${self.dollars} | {self.walls}"

    def build_menu(self, show_selector=True, refresh=False):
        if refresh:
            self.update_header()
        lines = super().build_menu()
        return lines


class GameMenu(Menu):

    def __init__(self):
        super().__init__()
        self.menu_name = "game_menu"
        self.header = " - Game Menu - "
        self.selected_item: str = "enter"
        self.menu_order = [
            "enter", "rob", "bank", "shop"
        ]
        self.actions = {
            "enter": {
                "message": "Enter House",
                "before": "shop",
                "after": "rob",
            },
            "rob": {
                "message": "Rob House",
                "before": "enter",
                "after": "shop"
            },
            "bank": {
                "message": "Rob Bank",
                "before": "rob",
                "after": "shop"
            },
            "shop": {
                "message": "Shop",
                "before": "rob",
                "after": "enter"
            }
        }


class InfoMenu(Menu):

    def __init__(self, lines):
        super().__init__()
        self.menu_name = "info"
        self.header = "  -- Info  --  "
        self.selected_item: str = ""
        self.menu_order = []
        self.lines = lines
        self.actions = {}
        self.format_lines()

    def format_lines(self):
        i: int = 0
        self.menu_order = []
        self.actions = {}
        for line in self.lines:
            self.menu_order.append(f"a{i}")
            self.actions[f"a{i}"] = line
            i += 1

    def refresh_lines(self):
        ip = atomics.NETWORK_IP if atomics.NETWORK_IP else "IP: -"
        mac = atomics.NETWORK_MAC if atomics.NETWORK_MAC else "MAC: -"
        ssid = atomics.NETWORK_SSID if atomics.NETWORK_SSID else "SSID: -"
        self.lines = [
            ssid, mac, ip
        ]
        if atomics.NETWORK_CONNECTED != "connected":
            self.lines = [
                "SSID: -", "MAC: -", "IP: -"
            ]

        self.format_lines()

    def build_menu(self, show_selector=False, refresh=False):
        self.refresh_lines()
        lines = super().build_menu()
        return lines


class AnimationMenu(Menu):

    def __init__(self):
        super().__init__()
        self.menu_name = "animations"
        self.header = " -- Animate -- "
        self.selected_item: str = "potato"
        self.menu_order = [item for item in ANIMATION_MAPPER]
        self.actions = {}
        for item in ANIMATION_MAPPER:
            chars = [c for c in item]
            chars[0] = chars[0].upper()
            self.actions[item] = "".join(chars)


class LightMenu(Menu):

    def __init__(self):
        super().__init__()
        self.menu_name = "lights"
        self.header = " -- Lights -- "
        self.selected_item: str = "off"
        self.menu_order = ["off", "green", "blue", "blink", "test", "adaptive"]
        self.modified = True

        # Todo: Figure out something smarter to do w/ the leds
        self.actions = {
            "off": "Off",
            "green": "Green",
            "blue": "Blue",
            "blink": "Blink",
            "test": "Test",
            "adaptive": "Adaptive"  # React to elements in game
        }
