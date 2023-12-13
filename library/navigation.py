

class Menu:

    def __init__(self):
        self.header = None
        self.menu_name = "Abstract"
        self.selected_item: str = "nop"
        self.menu_order = []
        self.actions = {
            "nop": {
                "message": "NOP",
                "next": "nop",
                "before": "nop"
            }
        }

    def increment_state(self):
        self.selected_item = self.actions[self.selected_item]["next"]
        return self.selected_item

    def decrement_state(self):
        self.selected_item = self.actions[self.selected_item]["before"]
        return self.selected_item

    def build_menu(self):
        lines = [] if not self.header else [self.header]
        for k in self.menu_order:
            item = self.actions[k]
            if "hidden" in item and item["hidden"]:
                continue
            message = f"{'>' if k == self.selected_item else ' '} {item['message']}"
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
            "info", "game", "settings"
        ]
        self.actions = {
            "info": {
                "message": "Info",
                "next": "game",
                "before": "settings"
            },
            "game": {
                "message": "Game",
                "next": "settings",
                "before": "info"
            },
            "settings": {
                "message": "Settings",
                "next": "info",
                "before": "game"
            },
            "none": {  # Prevents actions while in a locked state
                "message": "",
                "next": "info",  # If you get stuck in this state you can still increment
                "before": "info",
                "hidden": True
            }
        }


class GameMenu(Menu):

    def __init__(self):
        super().__init__()
        self.menu_name = "game_menu"
        self.header = " - Game Menu - "
        self.selected_item: str = "enter"
        self.menu_order = [
            "enter", "rob"
        ]
        self.actions = {
            "enter": {
                "message": "Enter House",
                "next": "rob",
                "before": "rob"
            },
            "rob": {
                "message": "Rob House",
                "next": "enter",
                "before": "enter"
            }
        }


class OfflineMenu(Menu):

    def __init__(self):
        super().__init__()
        self.menu_name = "offline"
        self.header = " -- Offline -- "
        self.selected_item: str = "nop"
        self.menu_order = []
        self.actions = {
            "nop": {
                "message": "NOP",
                "next": "potato",
                "before": "potato"
            },
            "potato": {
                "message": "NOP",
                "next": "nop",
                "before": "nop"
            }
        }
