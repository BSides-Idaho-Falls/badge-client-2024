import argparse
import os
import shutil
import time
from typing import List, Optional


FILES: List[str] = [
    "boot.py",
    "i2c_eeprom.py",
    "ssd1306.py",
    "initialization.py",
    "main.py",
    "display_helper.py",  # This takes a while to load, uncomment to load once
    "secrets.py",  # Make sure to add this!
]

DIRS: List[str] = [
    "__init__.py",
    "action_class.py",
    "actions_animation_menu.py",
    "actions_game.py",
    "actions_game_menu.py",
    "actions_info_menu.py",
    "actions_light_menu.py",
    "actions_main_menu.py",
    "actions_offline_menu.py",
    "actions_shop_menu.py",
    "atomics.py",
    "badge.py",
    "button_trigger.py",
    "buttons.py",
    "display.py",
    "fileio.py",
    "light_handler.py",
    "navigation.py",
    "networking.py"
]


POSSIBLE_DEVICE_LOCATIONS: List[str] = [
    "/dev/ttyUSB0",  # Location for linux
    "/dev/cu.usbmodem1401",  # Location behind USB hub on MacOS
    "/dev/cu.usbmodem101"  # Common location for MacOS
]

FIRM_LOC = "./firmware/rp2-pico-w-20230426-v1.20.0.uf2"


def flash_firm():
    shutil.copyfile('./rp2-pico-w-20230426-v1.20.0.uf2', f'{FIRM_LOC}rp2-pico-w-20230426-v1.20.0.uf2')
    input("Please unplug the badge and plug it back in, then hit enter to continue!")


def waitfor(seconds: int):
    print("Sleeping for ", end="")
    for i in range(seconds, 0, -1):
        print(f"{i} ", end="", flush=True)
        time.sleep(1)
    print("")


def detect_location(device: Optional[str]) -> Optional[str]:
    if device:
        if os.path.exists(device):
            return device
        else:
            print("Provided device location doesn't exist, attempting other locations.")
    for location in POSSIBLE_DEVICE_LOCATIONS:
        if os.path.exists(location):
            return location
    print("No device found.")
    return None


def make_dir(location, dir_name):
    try:
        os.system(f"ampy -p {location} mkdir {dir_name}")
    except Exception:
        pass


def write_single_file(location: str, file_name):
    if "library/" in file_name:
        # We'll add it back in if necessary
        file_name = file_name.replace("library/", "")
    if "." not in file_name:
        # No extension? We'll assume .py
        file_name = f"{file_name}.py"
    prefix: str = "library/" if file_name in DIRS else ""
    print(f"Writing file {file_name}")
    os.system(f"ampy -p {location} put {prefix}{file_name} /{prefix}{file_name}")


def write_files(args):
    location: str = detect_location(args.device)
    if not location:
        return
    make_dir(location, "library")
    if args.file:
        write_single_file(location, args.file)
        return
    for file_name in DIRS:
        write_single_file(location, file_name)
    if not args.library:
        for file_name in FILES:
            write_single_file(location, file_name)


def go(args):
    if not args.loop:
        if args.firmware:
            flash_firm()
        write_files(args)
        return
    print("Looping flash write")
    while True:
        if args.firmware:
            flash_firm()
        print("Starting flash...")
        write_files(args)
        print("Complete! Disconnect badge before restarting")
        waitfor(5)


def get_args():
    parser = argparse.ArgumentParser(
        prog='Badge Flasher',
        description='Flashes files onto the badge!'
    )
    parser.add_argument(
        '-l', '--loop', action='store_true', help='Flashes badges in a loop', default=False
    )
    parser.add_argument(
        '-lb', '--library', action='store_true', help='Write only files in the library directory', default=False
    )
    parser.add_argument(
        '-d', '--device', action='store', type=str, help='Device path to the badge (e.g. /dev/ttyUSB0', default=None
    )
    parser.add_argument(
        '-f', '--file', action='store', type=str, help='Write only one file', default=None
    )
    parser.add_argument(
        '-R', '--reset', action='store_true', help='FULL RESET. Deletes db.json & writes all files.', default=False
    )
    parser.add_argument(
        '-w', '--firmware', action='store_true', help='Flash Firmware!'
    )
    return parser.parse_args()


def validate_args(args) -> bool:
    if args.reset and args.file:
        print("Can't supply both --file AND --reset")
        return False
    if args.file and args.library:
        print("Can't supply both --file and --library")
        return False
    if args.reset and args.library:
        print("Can't supply both --reset and --library")
        return False
    return True


if __name__ == '__main__':
    args = get_args()
    if not validate_args(args):
        quit()
    go(args)
