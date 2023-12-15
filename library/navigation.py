

class Menu:

    def __init__(self):
        self.header = None
        self.menu_name = "Abstract"
        self.selected_item: str = "nop"
        self.menu_order = []
        self.modified = True
        self.actions = {
            "nop": {
                "message": "NOP",
                "next": "nop",
                "before": "nop"
            }
        }

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
            "info", "game", "animate"
        ]
        self.actions = {
            "info": {
                "message": "Info"
            },
            "game": {
                "message": "Game"
            },
            "animate": {
                "message": "Animations"
            },
            "none": {  # Prevents actions while in a locked state: DO NOT EDIT
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
                "message": "Enter House"
            },
            "rob": {
                "message": "Rob House"
            },
            "none": {  # Prevents actions while in a locked state: DO NOT EDIT
                "message": "",
                "next": "info",  # If you get stuck in this state you can still increment
                "before": "info",
                "hidden": True
            }
        }


class InfoMenu(Menu):

    def __init__(self, lines):
        super().__init__()
        self.menu_name = "info"
        self.header = "  -- Info  --  "
        self.selected_item: str = ""
        self.menu_order = []
        i = 0
        self.actions = {}
        for line in lines:
            self.menu_order.append(str(i))
            self.actions[str(i)] = {
                "message": line,
                "next": "0",
                "before": "0"
            }
            i += 1


class AnimationMenu(Menu):

    def __init__(self):
        super().__init__()
        self.menu_name = "animations"
        self.header = " -- Animate -- "
        self.selected_item: str = "potato"
        self.menu_order = [
            "potato"
        ]
        self.actions = {
            "potato": {
                "message": "Potato"
            },
            "none": {  # Prevents actions while in a locked state: DO NOT EDIT
                "message": "",
                "next": "info",  # If you get stuck in this state you can still increment
                "before": "info",
                "hidden": True
            }
        }
