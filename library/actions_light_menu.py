from library import atomics
from library.action_class import ButtonAction
from library.display import QueueItem
from library.light_handler import LightQueue
from library.light_patterns import LightPatterns
from library.navigation import MainMenu


class LightMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def action_forward(self):
        atomics.ANIMATE_MENU.increment_state()

    def action_backward(self):
        atomics.ANIMATE_MENU.decrement_state()

    def primary_select(self):
        selected_item: str = atomics.LIGHT_MENU.selected_item
        if selected_item == "off":
            atomics.LIGHTS.off()
            return
        atomics.LIGHTS.on()
        if selected_item == "green":
            green = LightPatterns.get_by_color("green")
            atomics.LIGHTS.queue_item(
                LightQueue(led_left=green, led_center=green, led_right=green)
            )
            return
        if selected_item == "blink":
            LightPatterns.get_pattern("blink_test", auto_queue=True)
            return
        if selected_item == "adaptive":
            atomics.LIGHTS.is_adaptive = not atomics.LIGHTS.is_adaptive
            enable_msg: str = "Enabled" if atomics.LIGHTS.is_adaptive else "Disabled"
            print(f"Adaptive Lighting: {enable_msg}")
            atomics.DISPLAY.queue_item(QueueItem("popup", {
                "delay": 2100,
                "message": [
                    "Adaptive:",
                    enable_msg
                ]
            }))

    def secondary_select(self):
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.LIGHT_MENU = None

