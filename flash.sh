#!/usr/bin/bash
if [[ -e /dev/cu.usbmodem101 ]];
    then
        echo "Found /dev/cu.usbmodem101... starting flash"

        ampy -p /dev/cu.usbmodem101 put boot.py
        ampy -p /dev/cu.usbmodem101 put i2c_eeprom.py
        ampy -p /dev/cu.usbmodem101 put ssd1306.py
        ampy -p /dev/cu.usbmodem101 put initialization.py

        ampy -p /dev/cu.usbmodem101 put main.py

        echo "Test Complete... disconnect!"
        sleep 3
    fi