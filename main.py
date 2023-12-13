import uasyncio as asyncio
import time
import _thread
import initialization as fu
from display import Display, QueueItem
from display_helper import WINKING_POTATO

i2c_h = fu.init_i2c()
fu.i2c_eeprom_init(i2c_h)
oled_h = fu.init_oled(i2c_h)


async def start_main():
    display: Display = Display(oled_h)
    _thread.start_new_thread(display.run, ())

    winking_potato = QueueItem("animation", WINKING_POTATO, 0.08)
    for i in range(0, 5):
        display.queue_item(winking_potato)
    display.queue_item(QueueItem("clear"))


if __name__ == '__main__':
    while True:
        asyncio.run(start_main())
        print("Restarting main thread...")
        time.sleep(1)
