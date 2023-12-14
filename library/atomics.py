from library.navigation import Menu

NETWORK_CONNECTED = "disconnected"
NETWORK_SSID = "N/A"
NETWORK_MAC = "N/A"
NETWORK_IP = "N/A"
NETWORK_MSGS = []

FREEZE_BUTTONS = False

DISPLAY = None

STATE = "main_menu"
STATE_TRACKING = {}

PB0 = None
PB1 = None

MAIN_MENU: Menu = None
GAME_MENU: Menu = None
INFO_MENU: Menu = None

