import uasyncio as asyncio
import initialization as fu
import neopixel
from library import atomics
from library.light_patterns import LightPatterns


class LightQueue:

    def __init__(self, led_left=None, led_center=None, led_right=None, delay: float = None):
        # If led is None, no update will be performed. This allows
        # for the updating of a singular LED
        self.led_left = led_left
        self.led_center = led_center
        self.led_right = led_right
        self.delay: float = delay or 0.5
        if self.delay < 0.1:
            self.delay = 0.1


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

    def adaptive_queue(self, queue_item: LightQueue):
        if not self.is_adaptive:
            return
        self.queue_item(queue_item)

    def off(self):
        self.is_off = True
        self.clear_queue()
        off_val = LightPatterns.get_off_value()
        self.queue_item(LightQueue(led_left=off_val, led_center=off_val, led_right=off_val))

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
        light_queue: LightQueue = self.queue.pop(0)
        await self.update_leds(light_queue)

    async def update_leds(self, light_queue: LightQueue):
        if light_queue.led_left:
            self.np[0] = light_queue.led_left
        if light_queue.led_center:
            self.np[1] = light_queue.led_center
        if light_queue.led_right:
            self.np[2] = light_queue.led_right
        self.np.write()
        await asyncio.sleep_ms(light_queue.delay)

