import json

import uasyncio as asyncio
import gc
import initialization as fu
import library.button_trigger as ba
from library import atomics, fileio
from library.buttons import Pushbutton
from library.display import Display, QueueItem
from display_helper import WINKING_POTATO
from library.light_handler import Lights
from library.navigation import MainMenu, OfflineMenu
from library.networking import Networking, Api

i2c_h = fu.init_i2c()
fu.i2c_eeprom_init(i2c_h)
oled_h = fu.init_oled(i2c_h)


def init_btns():
    # Initialize buttons from pins into buttons
    button1 = fu.machine.Pin(1, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP)
    button0 = fu.machine.Pin(0, fu.machine.Pin.IN, fu.machine.Pin.PULL_UP)

    # Initialize buttons into static variables in the atomics file.
    # Allows detecting press, double-press & long-press
    atomics.PB0 = Pushbutton(button0, suppress=True)
    atomics.PB1 = Pushbutton(button1, suppress=True)


def init_api():
    data = fileio.get_local_data()
    print(f"Read {json.dumps(data)}")

    # Required values
    atomics.API_REGISTRATION_TOKEN = data.get("registration_token", "")

    # Optional values
    atomics.API_TOKEN = data.get("api_token", "")
    atomics.API_PLAYER_ID = data.get("player_id", "")
    atomics.API_HOUSE_ID = data.get("house_id", "")

    fileio.write_local_data(data)


async def btn_listener():
    # Grab the buttons as defined in init_btns
    btn_right = atomics.PB0
    btn_left = atomics.PB1
    if not btn_right or not btn_left:
        print("Error init buttons")
        return

    # List of actions and what they do can be found in /library/button_trigger.py

    # Short press btn_right -> action_forward
    btn_right.release_func(ba.action_forward, ())

    # Short press btn_left -> action_backward
    btn_left.release_func(ba.action_backward, ())

    # Long press btn_right -> primary_select
    btn_right.long_func(ba.primary_select, ())

    # Long press btn_left -> secondary_select
    btn_left.long_func(ba.secondary_select, ())

    # Double press btn_right -> secondary_modify
    btn_right.double_func(ba.secondary_modify, ())

    # Double press btn_left -> primary_modify
    btn_left.double_func(ba.primary_modify, ())

    # Hybrid actions also exist. For example, move a player right in their house
    # example_btn_move_right.release_func(ba.hybrid_action_move, ("right"))

    await asyncio.sleep_ms(1000)


async def screen_updater(display: Display):
    while True:
        await display.run()


def configure_api():
    local_data = fileio.get_local_data()
    if "registration_token" not in local_data or local_data["registration_token"] == "":
        print("Attempting registration (id=1)")
        atomics.API_CLASS.attempt_self_register(auto_write=True)
    s1 = atomics.API_CLASS.create_player()
    if not s1:
        return False
    s2 = atomics.API_CLASS.create_house()
    return s1 and s2


async def light_queue(lights: Lights):
    while True:
        atomics.feed()
        await lights.run()


async def display_queue(display: Display):
    atomics.MAIN_MENU = MainMenu()
    atomics.OFFLINE_MENU = OfflineMenu()
    first_menu = True
    first_connection = False
    api_configured = False
    while True:
        atomics.feed()
        if atomics.NETWORK_CONNECTED != "connected" or not api_configured:
            if atomics.NETWORK_CONNECTED == "connected":
                api_configured = configure_api()
            if atomics.STATE == "main_menu":
                # Other menus don't need to context switch
                atomics.STATE = "offline_menu"
            can_queue = first_menu
            lines = []
            if atomics.STATE == "offline_menu":
                lines = atomics.OFFLINE_MENU.build_menu()
                if atomics.OFFLINE_MENU.modified:
                    can_queue = True
                    atomics.OFFLINE_MENU.modified = False
            elif atomics.STATE == "info_menu":
                lines = atomics.INFO_MENU.build_menu()
                lines.insert(1, f"Tries: {atomics.NETWORK_CONNECT_ATTEMPTS}")
                if atomics.INFO_MENU.modified:
                    can_queue = True
                    atomics.INFO_MENU.modified = False
            elif atomics.STATE == "animate_menu":
                lines = atomics.ANIMATE_MENU.build_menu()
                if atomics.ANIMATE_MENU.modified:
                    can_queue = True
                    atomics.ANIMATE_MENU.modified = False
            elif atomics.STATE == "light_menu":
                lines = atomics.LIGHT_MENU.build_menu(refresh=True)
                if atomics.LIGHT_MENU.modified:
                    can_queue = True
                    atomics.LIGHT_MENU.modified = False
            queue_item = QueueItem("text", data={
                "message": lines
            })
            if can_queue:
                display.queue_item(queue_item)
                first_menu = False
        elif atomics.NETWORK_CONNECTED == "connected":
            if not api_configured:
                api_configured = configure_api()
                continue
            if atomics.STATE == "offline_menu":
                atomics.STATE = "main_menu"  # Automatic context switching
            lines = []
            can_queue = first_menu
            if not first_connection:
                first_connection = True
                can_queue = True

            # TODO: Abstract the menu generation
            # Ensure it's for menu's only, and abstraction doesn't
            # attempt to override game visualization to prevent
            # over-queueing

            if atomics.STATE == "main_menu":
                lines = atomics.MAIN_MENU.build_menu()
                if atomics.MAIN_MENU.modified:
                    can_queue = True
                    atomics.MAIN_MENU.modified = False
            elif atomics.STATE == "game_menu":
                lines = atomics.GAME_MENU.build_menu()
                if atomics.GAME_MENU.modified:
                    can_queue = True
                    atomics.GAME_MENU.modified = False
            elif atomics.STATE == "shop_menu":
                lines = atomics.SHOP_MENU.build_menu(refresh=True)
                if atomics.SHOP_MENU.modified:
                    can_queue = True
                    atomics.SHOP_MENU.modified = False
            elif atomics.STATE == "info_menu":
                lines = atomics.INFO_MENU.build_menu()
                if atomics.INFO_MENU.modified:
                    can_queue = True
                    atomics.INFO_MENU.modified = False
            elif atomics.STATE == "animate_menu":
                lines = atomics.ANIMATE_MENU.build_menu()
                if atomics.ANIMATE_MENU.modified:
                    can_queue = True
                    atomics.ANIMATE_MENU.modified = False
            queue_item = QueueItem("text", data={
                "message": lines
            })
            if can_queue:
                display.queue_item(queue_item)
                first_menu = False
        await asyncio.sleep_ms(30)


async def start_main():
    atomics.DISPLAY = Display(oled_h)
    atomics.LIGHTS = Lights()
    atomics.API_CLASS = Api()
    networking: Networking = Networking()
    init_btns()
    asyncio.create_task(screen_updater(atomics.DISPLAY))

    atomics.DISPLAY.queue_item(QueueItem("animation", WINKING_POTATO, 30))

    asyncio.create_task(networking.run())
    init_api()
    asyncio.create_task(btn_listener())
    asyncio.create_task(display_queue(atomics.DISPLAY))

    while True:
        await asyncio.sleep_ms(5000)
        gc.collect()
