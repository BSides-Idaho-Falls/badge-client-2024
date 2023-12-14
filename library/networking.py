import json
import time

import secrets
import network
import urequests
import ubinascii
import uasyncio as asyncio

from library import atomics, fileio


class Api:

    def __init__(self):
        self.base_url = atomics.API_BASE_URL
        self.in_house = False

    def _make_request(self, method, url, headers=None, data=None):
        if data is None:
            data = {}
        print(f"--> URL: {method} {url}")
        print(f"--> Headers: {json.dumps(headers)}")
        print(f"--> Payload: {json.dumps(data)}")
        response = urequests.request(method, url, headers=headers, data=data)
        response_data = response.json()
        print(f"<-- {json.dumps(response_data)}")
        return response_data

    def move(self, direction):
        if direction not in ["left", "right", "up", "down"]:
            return None
        if not atomics.NETWORK_MAC:
            print("no mac")
            return None
        if not atomics.API_PLAYER_ID:
            print("no player_id")
            return None
        if not self.in_house:
            print("Not in house")
            return None
        headers = {
            "X-API-Token": atomics.API_TOKEN
        }
        url = f"{self.base_url}/api/game/{atomics.API_PLAYER_ID}/move/{direction}"
        response = self._make_request("POST", url, headers=headers)
        return response


    def enter_house(self):
        if not atomics.NETWORK_MAC:
            print("Failed to enter house because there's no network!")
            return None
        if not atomics.API_PLAYER_ID:
            print("Failed to enter house because there's no player")
            return None
        url = f"{self.base_url}/api/game/{atomics.API_PLAYER_ID}/enter_house"
        headers = {
            "X-API-Token": atomics.API_TOKEN
        }
        response_data = self._make_request("POST", url, headers=headers)
        if response_data["success"]:
            self.in_house = True
        return response_data

    def leave_house(self):
        if not atomics.NETWORK_MAC:
            print("Failed to leave house because there's no network!")
            return None
        if not atomics.API_PLAYER_ID:
            print("Failed to leave house because there's no player")
            return None
        url = f"{self.base_url}/api/game/{atomics.API_PLAYER_ID}/leave_house"
        headers = {
            "X-API-Token": atomics.API_TOKEN
        }
        response_data = self._make_request("POST", url, headers=headers)
        if response_data["success"]:
            self.in_house = False
        return response_data




    def create_house(self):
        if not atomics.NETWORK_MAC:
            print("Failed to create house because there's no network!")
            return False
        if not atomics.API_PLAYER_ID:
            print("Failed to create house because there's no player")
            return False

        player_id = atomics.API_PLAYER_ID
        url = f"{self.base_url}/api/house/{player_id}"
        headers = {
            "X-API-Token": atomics.API_TOKEN
        }
        response_data = self._make_request("POST", url, headers=headers)
        if response_data["success"]:
            atomics.API_HOUSE_ID = response_data["house_id"]
            db = fileio.get_local_data()
            db["house_id"] = atomics.API_HOUSE_ID
            fileio.write_local_data(db)
        return True

    def create_player(self):
        if not atomics.NETWORK_MAC:
            print("Failed to create player because there's no network!")
            return False
        player_id = atomics.NETWORK_MAC
        url = f"{self.base_url}/api/player/{player_id}"
        headers = {
            "X-Register-Token": atomics.API_REGISTRATION_TOKEN
        }
        response_data = self._make_request("POST", url, headers=headers)
        if response_data["success"]:
            atomics.API_TOKEN = response_data["token"]
            atomics.API_PLAYER_ID = response_data["player_id"]
            db = fileio.get_local_data()
            db["api_token"] = response_data["token"]
            db["player_id"] = response_data["player_id"]
            fileio.write_local_data(db)
        return True



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
            attempts_left = 5
            while not self.wlan.isconnected() or attempts_left > 0:
                attempts_left = attempts_left - 1
                time.sleep(1)
            if not self.wlan.isconnected():
                print(f"Failed to connect to {ssid}")
                continue
            wlan_mac = self.wlan.config('mac')
            self.mac = ubinascii.hexlify(wlan_mac).decode()
            self.ip = self.wlan.ifconfig()[0]
            self.network_status = "connected"
            self.wifi_details = item
            print(f"Connected to {ssid}! IP: {self.ip}, MAC: {self.mac}")
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




