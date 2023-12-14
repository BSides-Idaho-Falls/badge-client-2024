import os
import sys
import time
from typing import List, Optional

# secrets.py sample:

# CREDS = [
#     {
#         "ssid": "ssid",
#         "password": "some-password-here"
#     }
# ]


FILES: List[str] = [
    # "boot.py",
    # "i2c_eeprom.py",
    # "ssd1306.py",
    # "initialization.py",
    # "main.py",
    #"display_helper.py",  # This takes a while to load, uncomment to load once
    #"secrets.py",  # Make sure to add this!
]

DIRS: List[str] = [
    # "library/__init__.py",
    "library/atomics.py",
    "library/display.py",
    # "library/networking.py",
    # "library/buttons.py",
    "library/badge.py",
    "library/button_actions_base.py",
    "library/navigation.py",
    "library/fileio.py"
]

POSSIBLE_DEVICE_LOCATIONS: List[str] = [
    "/dev/cu.usbmodem101"  # Common location for MacOS
]


def waitfor(seconds: int):
    print("Sleeping for ", end="")
    for i in range(seconds, 0, -1):
        print(f"{i} ", end="", flush=True)
        time.sleep(1)
    print("")


def detect_location() -> Optional[str]:
    for location in POSSIBLE_DEVICE_LOCATIONS:
        if os.path.exists(location):
            return location
    return None


def make_dir(location, dir_name):
    try:
        os.system(f"ampy -p {location} mkdir {dir_name}")
    except Exception:
        pass


def start_flash(location: str, single_file: str = None):
    if single_file:
        print(f"Writing {single_file}")
        os.system(f"ampy -p {location} put {single_file}")
        return
    print("Writing ", end="")
    i = 0
    for file in FILES:
        i += 1
        print(file, end="")
        if file != FILES[-1]:
            print(", ", end="", flush=True)
        if i > 0 and i % 5 == 0:
            print("")
        os.system(f"ampy -p {location} put {file}")
    i = 0
    for directory in DIRS:
        i += 1
        print(directory, end="")
        if directory != DIRS[-1]:
            print(", ", end="", flush=True)
        if i > 0 and i % 5 == 0:
            print("")
        os.system(f"ampy -p {location} put {directory} /{directory}")

    print("")


def init():
    location: Optional[str] = detect_location()
    if location is None:
        print("No badge location found!")
        return
    print(f"Found location: {location}")
    single_file: Optional[str] = None
    loop: bool = "-loop" in sys.argv or "--loop" in sys.argv
    if len(sys.argv) > 1:  # sys.argv[0] is the python script name itself
        if "-loop" not in sys.argv[1] and "--loop" not in sys.argv[1]:
            single_file = sys.argv[1]
    if loop:
        print("Looping flash write")
        while True:
            print("Starting flash...")
            start_flash(location, single_file=single_file)
            print("Complete! Disconnect badge before restarting")
            waitfor(5)
    else:
        print("Starting flash...")
        start_flash(location, single_file=single_file)
        print("Complete!")


if __name__ == '__main__':
    init()
