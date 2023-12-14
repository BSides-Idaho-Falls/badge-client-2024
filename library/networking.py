import time

import secrets
import network
import ubinascii
import uasyncio as asyncio

from library import atomics


class Api:

    def __init__(self):
        pass


class Networking:

    def __init__(self):
        self.wifi_details: dict = None
        self.network_creds = secrets.CREDS
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan_handle = None
        self.mac = None
        self.ip = None
        self.network_status = "disconnected"

    def determine_wifi(self):
        for item in self.network_creds:
            self.wlan.active(True)
            ssid, password = item["ssid"], item["password"]
            print(f"Checking wifi ssid {ssid}...")
            self.wlan_handle = self.wlan.connect(ssid, password)
            wlan_mac = self.wlan.config('mac')
            self.mac = ubinascii.hexlify(wlan_mac).decode()
            self.ip = self.wlan.ifconfig()[0]
            attempts_left = 5
            while not self.wlan.isconnected() or attempts_left > 0:
                attempts_left = attempts_left - 1
                time.sleep(1)
            if not self.wlan.isconnected():
                print(f"Failed to connect to {ssid}")
                continue
            self.network_status = "connected"
            self.wifi_details = item
            print(f"Connected to {ssid}!")
            return item
        return None

    def connection(self):
        if not self.wifi_details:
            if not self.determine_wifi():
                return
        if not self.wlan.isconnected():
            self.network_status = "disconnected"
            ssid, password = self.wifi_details["ssid"], self.wifi_details["password"]
            print("Wifi disconnected, reattempting connection")
            self.wlan_handle = self.wlan.connect(ssid, password)
            wlan_mac = self.wlan.config('mac')
            self.mac = ubinascii.hexlify(wlan_mac).decode()
        else:
            self.network_status = "connected"
            wlan_mac = self.wlan.config('mac')
            self.mac = ubinascii.hexlify(wlan_mac).decode()
            self.ip = self.wlan.ifconfig()[0]

    def tick(self):
        self.connection()  # Test wifi connection, attempt reconnections
        self.update_wifi_atomics()

    def update_wifi_atomics(self):
        atomics.NETWORK_CONNECTED = self.network_status
        if not self.wifi_details:
            atomics.NETWORK_SSID = "N/A"
        atomics.NETWORK_SSID = self.wifi_details["ssid"]
        if self.ip:
            atomics.NETWORK_IP = self.ip
        if self.mac:
            atomics.NETWORK_MAC = self.mac

    async def run(self):
        while True:
            self.tick()
            await asyncio.sleep_ms(500)




