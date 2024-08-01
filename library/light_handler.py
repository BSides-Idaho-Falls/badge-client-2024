import uasyncio as asyncio
import initialization as fu
import neopixel
from library import atomics


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
                LightQueue(green, off, green, 100),
                LightQueue(off, green, off, 1000),
                LightQueue(blue, off, blue, 100),
                LightQueue(off, blue, off, 100)
            ],
            "blink_red": [
                LightQueue(off, off, off, 300),
                LightQueue(red, red, red, 500),
                LightQueue(off, off, off, 200)
            ],
            "rob_success": [
                LightQueue(green, green, green, 700),
                LightQueue(off, off, off, 500),
                LightQueue(green, green, green, 500),
                LightQueue(blue, blue, blue, 700),
                LightQueue(off, off, off, 500),
                LightQueue(green, green, green, 800),
                LightQueue(off, off, off, 500)
            ]
        }
        if name not in patterns:
            return []
        if auto_queue:
            for item in patterns[name]:
                atomics.LIGHTS.queue_item(item)
        return patterns[name]


class LightQueue:

    def __init__(self, led_left=None, led_center=None, led_right=None, delay: int = None):
        # If led is None, no update will be performed. This allows
        # for the updating of a singular LED
        self.led_left = led_left
        self.led_center = led_center
        self.led_right = led_right
        self.delay: int = delay or 500
        if self.delay < 10:
            self.delay = 10


class Lights:

    def __init__(self):
        self.queue: list = []
        self.is_off = True
        self.is_adaptive = False
        self.np = neopixel.NeoPixel(
            fu.machine.Pin(atomics.NEOPIXEL_PIN, fu.machine.Pin.OUT),
            atomics.NEOPIXEL_COUNT
        )

    def queue_item(self, queue_item: LightQueue):
        if self.is_off:
            return
        self.queue.append(queue_item)

    def adaptive_queue(self, queue_item):
        if not self.is_adaptive:
            return
        if isinstance(queue_item, list):
            for item in queue_item:
                self.queue_item(item)
            return
        self.queue_item(queue_item)

    def off(self):
        self.clear_queue()
        off_val = LightPatterns.get_off_value()
        self.queue_item(LightQueue(led_left=off_val, led_center=off_val, led_right=off_val))
        self.is_off = True

    def on(self, start_from: LightQueue = None):
        self.is_off = False
        if start_from:
            self.queue_item(start_from)

    def clear_queue(self):
        self.queue = []

    async def run(self):
        atomics.feed()
        if len(self.queue) < 1:
            await asyncio.sleep_ms(300)
            return
        await self.execute_queue_item()

    async def execute_queue_item(self):
        if len(self.queue) < 1:
            return
        light_queue: LightQueue = self.queue.pop(0)
        await self.update_leds(light_queue)

    async def update_leds(self, light_queue: LightQueue):
        # TODO: Determine actual LED order
        if light_queue.led_left:
            self.np[0] = light_queue.led_left
        if light_queue.led_center:
            self.np[1] = light_queue.led_center
        if light_queue.led_right:
            self.np[2] = light_queue.led_right
        self.np.write()
        await asyncio.sleep_ms(light_queue.delay)

