import argparse
import os
import time
from typing import List, Optional
import shutil

FILES: List[str] = [
    "main.py",
    "ssd1306.py"
]

DIRS: List[str] = [
]

FIRM_LOC =     "/media/spectre03/RPI-RP2/"  # Location for linux

POSSIBLE_DEVICE_LOCATIONS: List[str] = [
    "/dev/ttyUSB0",  # Location for linux
    "/dev/ttyACM0",  # Location for linux
    "/dev/cu.usbmodem1401",  # Location behind USB hub on MacOS
    "/dev/cu.usbmodem101"  # Common location for MacOS
]

def flash_firm():
    shutil.copyfile('./rp2-pico-w-20230426-v1.20.0.uf2', f'{FIRM_LOC}rp2-pico-w-20230426-v1.20.0.uf2')

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
    # make_dir(location, "library")
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
        write_files(args)
        return
    print("Looping flash write")
    while True:
        print("Starting flash...")
        if os.path.exists(FIRM_LOC):
            print("New badge found... Flashing!")
            flash_firm()
            print("Done Flashing!")
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
