from library.navigation import Menu
from library.networking import Api

NETWORK_CONNECTED = "disconnected"
NETWORK_SSID = "N/A"
NETWORK_MAC = "N/A"
NETWORK_IP = "N/A"
NETWORK_MSGS = []

API_CLASS: Api = None

FREEZE_BUTTONS = False

DISPLAY = None

STATE = "main_menu"
STATE_TRACKING = {}

PB0 = None
PB1 = None

MAIN_MENU: Menu = None
GAME_MENU: Menu = None
INFO_MENU: Menu = None


API_BASE_URL = "http://10.10.0.10:8080"
API_REGISTRATION_TOKEN = ""
API_TOKEN = ""
API_PLAYER_ID = ""
API_HOUSE_ID = ""
