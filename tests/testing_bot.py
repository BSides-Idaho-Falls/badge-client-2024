import json
import time
import uuid

import requests

player_id = str(uuid.uuid4())

def register_player(player_id):
  url = f"http://localhost:8080/api/player/{player_id}"
  payload = {}
  headers = {
    'X-Register-Token': '217948849559'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  response_json = json.loads(response.text)
  token = response_json.get("token")
  print(response.text)
  return token


def create_house(player_id, token):
  url = f"http://localhost:8080/api/house/{player_id}"

  payload = {}
  headers = {
    'X-API-Token': token
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  response_json = json.loads(response.text)
  house_id = response_json.get("house_id")
  print(response.text)
  return house_id


def enter_house(player_id, token):
  url = f"http://localhost:8080/api/game/{player_id}/enter_house"

  payload = {}
  headers = {
    'c': 'y',
    'X-API-Token': token
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)


def leave_house(player_id, token):
  url = f"http://localhost:8080/api/game/{player_id}/leave_house"

  payload = {}
  headers = {
    'X-API-Token': token
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)


def move_in_house(player_id, token, direction):
  url = f"http://localhost:8080/api/game/{player_id}/move/{direction}"

  payload = {}
  headers = {
    'X-API-Token': token
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)


TOKEN = register_player(player_id)
HOUSE_ID = create_house(player_id, TOKEN)

enter_house(player_id, TOKEN)

move_in_house(player_id, TOKEN, "right-c")
move_in_house(player_id, TOKEN, "right-c")
direction = "right-c"
for i in range(0, 240):
  move_in_house(player_id, TOKEN, direction)
  if direction == "right-c":
    direction = "left-c"
  else:
    direction = "right-c"
  time.sleep(0.5)

leave_house(player_id, TOKEN)



