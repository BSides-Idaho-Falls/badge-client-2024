import json
import random

import network
import uasyncio as asyncio
import ubinascii
import urequests
import urandom
import hashlib

import secrets
from library import atomics, fileio


class Api:

    def __init__(self):
        self.base_url = atomics.API_BASE_URL
        self.in_house = False

    def _make_request(self, method, url, headers=None, data=None):
        if data is None:
            data = {}
        if headers is None:
            headers = {}
        print(f"--> URL: {method} {url}")
        print(f"--> Headers: {json.dumps(headers)}")
        print(f"--> Payload: {json.dumps(data)}")
        response = urequests.request(method, url, headers=headers, json=data)
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

    def enter_house_error_handler(self, response_data):
        already_inside_message = "You are already in the house!"
        if not ("reason" in response_data and response_data["reason"] == already_inside_message):
            return response_data
        self.leave_house()
        return self.enter_house()

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
        return self.enter_house_error_handler(response_data)

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

    def luhn_checksum(self, number: str) -> int:
        numbers: list = [c for c in number]
        total_sum: int = 0
        for i, digit in enumerate(reversed(numbers)):
            digit = int(digit)
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total_sum += digit
        checksum_digit = (10 - (total_sum % 10)) % 10
        return checksum_digit

    def check_luhn(self, number: str) -> bool:
        try:
            # Ensure number string is a valid number before passing to checksum
            # Yes, argument is passed in via string and not integer ;)
            int(number)
        except ValueError as _:
            return False
        return self.luhn_checksum(number) == 0

    def generate_luhn(self, size: int) -> str:
        random_number: str = "".join([str(random.randint(0, 9)) for _ in range(size - 1)])
        # 0 is not a typo, it's padding for the checksum
        checksum_digit = self.luhn_checksum(f"{random_number}0")
        luhn = f"{random_number}{checksum_digit}"
        return luhn

    def attempt_self_register(self, auto_write=False):
        if not atomics.NETWORK_MAC:
            print("Failed to register because there's no network!")
            return None
        if not atomics.NETWORK_CONNECTED:
            print("Failed to register because there's no network!")
            return None
        registration_token = self.generate_luhn(12)
        print(f"Registering {atomics.NETWORK_MAC} with registration token {registration_token}")
        player_id: str = atomics.NETWORK_MAC

        body = {
            "_id": registration_token,
            "mac": player_id
        }
        url = f"{self.base_url}/api/self-register"
        response_data = self._make_request("POST", url, data=body)
        if response_data["success"]:
            if auto_write:
                local_data = fileio.get_local_data()
                atomics.API_REGISTRATION_TOKEN = registration_token
                local_data["registration_token"] = registration_token
                fileio.write_local_data(local_data)
            return registration_token
        return None

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

    async def determine_wifi(self):
        for item in self.network_creds:
            self.wlan.active(True)
            ssid, password = item["ssid"], item["password"]
            print(f"Checking wifi ssid {ssid}...")
            self.wlan_handle = self.wlan.connect(ssid, password)
            attempts_left = 5 if atomics.NETWORK_CONNECT_ATTEMPTS < 3 else 6
            while not self.wlan.isconnected() and attempts_left > 0:
                attempts_left = attempts_left - 1
                print(f"Connect failed, retrying... {attempts_left}")
                await asyncio.sleep_ms(900 if atomics.NETWORK_CONNECT_ATTEMPTS < 3 else 1750)
            if not self.wlan.isconnected():
                print(f"Failed to connect to {ssid}")
                atomics.NETWORK_CONNECT_ATTEMPTS += 1
                if atomics.INFO_MENU:
                    atomics.INFO_MENU.modified = True
                continue
            atomics.NETWORK_CONNECT_ATTEMPTS = 0
            wlan_mac = self.wlan.config('mac')
            self.mac = ubinascii.hexlify(wlan_mac).decode()
            self.ip = self.wlan.ifconfig()[0]
            self.network_status = "connected"
            self.wifi_details = item
            print(f"Connected to {ssid}! IP: {self.ip}, MAC: {self.mac}")
            return item
        return None

    async def connection(self):
        wlan_mac = self.wlan.config('mac')
        self.mac = ubinascii.hexlify(wlan_mac).decode()
        atomics.NETWORK_MAC = self.mac
        if not self.wifi_details:
            await self.determine_wifi()
            if not self.wifi_details:
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

    async def tick(self):
        await self.connection()  # Test wifi connection, attempt reconnections
        self.update_wifi_atomics()

    def update_wifi_atomics(self):
        atomics.NETWORK_CONNECTED = self.network_status
        if not self.wifi_details:
            atomics.NETWORK_SSID = "SSID: -"
        else:
            atomics.NETWORK_SSID = self.wifi_details["ssid"]
        if self.ip:
            atomics.NETWORK_IP = self.ip
        else:
            atomics.NETWORK_IP = "IP: -"
        if self.mac:
            atomics.NETWORK_MAC = self.mac
        else:
            atomics.NETWORK_MAC = "Mac: -"

    async def run(self):
        while True:
            await self.tick()
            await asyncio.sleep_ms(500)
