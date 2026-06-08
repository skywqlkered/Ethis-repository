import requests
import base64
from mcname_api import get_uuid, get_username
import sys
import os

username = input("username: ")
uuid = get_uuid(username)
url = f"https://minotar.net/helm/{username}/256.png"

response = requests.get(url)
# print(response.content)
if response.status_code == 200:
    with open(f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/skins/{get_username(uuid)}.png", "wb") as f:
        f.write(response.content)
        print("Skin saved")