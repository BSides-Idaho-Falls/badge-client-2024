import uasyncio as asyncio
import gc
import initialization as fu
from library import atomics
from library.display import Display, QueueItem
from display_helper import WINKING_POTATO
from library.networking import Networking

i2c_h = fu.init_i2c()
fu.i2c_eeprom_init(i2c_h)
oled_h = fu.init_oled(i2c_h)


async def screen_updater(display: Display):
    while True:
        await display.run()


async def start_main():
    display: Display = Display(oled_h)
    networking: Networking = Networking()

    asyncio.create_task(screen_updater(display))
    asyncio.create_task(networking.run())

    display.queue_item(QueueItem("animation", WINKING_POTATO, 30))

    while True:
        display.queue_item(QueueItem("text", data={
            "message": [
                atomics.NETWORK_CONNECTED,
                atomics.NETWORK_SSID
            ]
        }))
        await asyncio.sleep_ms(5000)
        gc.collect()
