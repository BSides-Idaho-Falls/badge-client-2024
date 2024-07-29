from library import atomics
from library.light_handler import LightQueue


class LightPatterns:

    def __init__(self):
        pass

    @staticmethod
    def get_off_value():
        return LightPatterns.get_by_color("off")

    @staticmethod
    def get_by_color(color: str):
        bri: int = 20
        color_mappings: dict = {
            "red": (bri, 0, 0),
            "green": (0, bri, 0),
            "blue": (0, 0, bri),
            "white": (bri, bri, bri),
            "off": (0, 0, 0)
        }
        if color not in color_mappings:
            print("[warning] Unknown color mapping!")
            return 0, 0, 0
        return color_mappings[color]

    @staticmethod
    def get_pattern(name: str, auto_queue: bool = False) -> list:
        bri: int = 20
        off = LightPatterns.get_by_color("off")
        red = LightPatterns.get_by_color("red")
        green = LightPatterns.get_by_color("green")
        blue = LightPatterns.get_by_color("blue")
        patterns: dict = {
            "blink_test": [
                LightQueue(green, off, green, 1.0),
                LightQueue(off, green, off, 1.0),
                LightQueue(blue, off, blue, 1.0),
                LightQueue(off, blue, off, 1.0)
            ],
            "blink_red": [
                LightQueue(off, off, off, 0.3),
                LightQueue(red, red, red, 0.5),
                LightQueue(off, off, off, 0.2)
            ]
        }
        if name not in patterns:
            return []
        if auto_queue:
            for item in patterns[name]:
                atomics.LIGHTS.queue_item(item)
        return patterns[name]
