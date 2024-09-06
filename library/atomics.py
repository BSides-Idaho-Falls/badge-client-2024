"""This file is here because i'm lazy. Globally accessible variables!!!"""
from library.actions_game import GameState
from library.navigation import Menu
from library.networking import Api
import machine

API_BASE_URL = "http://api-bsides.meecles.io"
NEOPIXEL_PIN = 6
NEOPIXEL_COUNT = 3
WDT_ENABLED: bool = False

# The values immediately below are for button initialization.
# If you rename them, you will also need to adjust these values in
# badge.py::init_btns() and badge.py::btn_listener

PB0 = None  # Right button (B)
PB1 = None  # Left button (A)


# Dpad buttons
PB2 = None
PB3 = None
PB4 = None
PB5 = None

BADGE_YEAR = "2024"  # 2023 if you have the badge from 2023! :)

### DO NOT EDIT ANY VALUES BELOW THIS LINE ###
# These values are all modified by the application

NETWORK_CONNECTED = "disconnected"
NETWORK_SSID = "SSID: -"
NETWORK_MAC = "Mac: -"
NETWORK_IP = "IP: -"
NETWORK_MSGS = []
NETWORK_CONNECT_ATTEMPTS = 0

API_CLASS: Api = None
wdt = None

FREEZE_BUTTONS = False

DISPLAY = None
LIGHTS = None

STATE = "main_menu"
STATE_TRACKING = {}

MAIN_MENU: Menu = None
GAME_MENU: Menu = None
INFO_MENU: Menu = None
LIGHT_MENU: Menu = None
ANIMATE_MENU: Menu = None
OFFLINE_MENU: Menu = None
SHOP_MENU: Menu = None
GAME_STATE: GameState = None

KONAMI_PRESSES = []
EXPECTED_KONAMI = ["up", "up", "down", "down", "left", "right", "left", "right", "b", "a"]


# Yes including these! Do not edit these! (or do, idk)
API_REGISTRATION_TOKEN = ""
API_TOKEN = ""
API_PLAYER_ID = ""
API_HOUSE_ID = ""


def feed():
    global wdt
    if wdt and WDT_ENABLED:
        wdt.feed()
    else:
        if WDT_ENABLED:
            wdt = machine.WDT(timeout=3000)


def starve():
    global wdt
    if wdt:
        machine.mem32[0x40058000] = machine.mem32[0x40058000] & ~(1 << 30)
        wdt = None


def most_recent():
    return BADGE_YEAR == "2024"
