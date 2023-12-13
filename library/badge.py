import uasyncio as asyncio
import gc
import initialization as fu
import library.button_actions_base as ba
from library import atomics
from library.buttons import Pushbutton
from library.display import Display, QueueItem
from display_helper import WINKING_POTATO
from library.navigation import MainMenu, OfflineMenu
from library.networking import Networking

i2c_h = fu.init_i2c()
fu.i2c_eeprom_init(i2c_h)
oled_h = fu.init_oled(i2c_h)


def init_btns():
    button1 = fu.machine.Pin(1, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP)
    button0 = fu.machine.Pin(0, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP)
    atomics.PB0 = Pushbutton(button0, suppress=True)
    atomics.PB1 = Pushbutton(button1, suppress=True)


async def btn_listener():
    pb0 = atomics.PB0
    pb1 = atomics.PB1
    if not pb0 or not pb1:
        print("Error init buttons")
        return

    # press actions
    pb0.release_func(ba.press0, ())
    pb1.release_func(ba.press1, ())

    # long press actions
    pb0.long_func(ba.long_press0, ())
    pb1.long_func(ba.long_press1, ())

    # double press actions
    pb0.double_func(ba.double_press0, ())
    pb1.double_func(ba.double_press1, ())
    await asyncio.sleep_ms(1000)


async def screen_updater(display: Display):
    while True:
        await display.run()


async def display_queue(display: Display):
    atomics.MAIN_MENU = MainMenu()
    while True:
        queue_item = QueueItem("text", data={
            "message": [
                " -- Offline -- "
            ],
            "delay": 50
        })
        if atomics.NETWORK_CONNECTED == "connected":
            lines = []
            if atomics.STATE == "main_menu":
                lines = atomics.MAIN_MENU.build_menu()
            elif atomics.STATE == "game_menu":
                lines = atomics.GAME_MENU.build_menu()
            queue_item = QueueItem("text", data={
                "message": lines
            })

        display.queue_item(queue_item)
        await asyncio.sleep_ms(30)


async def start_main():
    display: Display = Display(oled_h)
    networking: Networking = Networking()
    init_btns()

    asyncio.create_task(screen_updater(display))

    display.queue_item(QueueItem("animation", WINKING_POTATO, 30))

    asyncio.create_task(networking.run())
    asyncio.create_task(btn_listener())
    asyncio.create_task(display_queue(display))

    while True:
        await asyncio.sleep_ms(5000)
        gc.collect()
