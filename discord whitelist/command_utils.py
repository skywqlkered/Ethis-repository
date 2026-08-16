import os

import requests
from dotenv import load_dotenv
from whitelist_utils import Whitelist


def onWhitelist(username: str):
    whitelist = Whitelist()
    usernames = whitelist.usernames
    return username in usernames

def send_whitelist_post(username: str):
    load_dotenv()

    bloom_secret = os.getenv("BLOOM_SECRET")
    url = "https://mc.bloom.host/api/client/servers/645aee1d/command"
    command = {"command": f"whitelist add {username}"}

    #use the 'headers' parameter to set the HTTP headers:
    x = requests.post(url, json=command, headers={"Authorization": f"Bearer {bloom_secret}"})

    return x.status_code

def add_user_to_whitelist(name):
    code =  send_whitelist_post(name)
    if code != 204:
        return "Bloom command failed with error code: ", code
        
    if onWhitelist(name):
        return f"Added {name} to the whitelist"
    else:
        return "User could not be added to the whitelist"
        
if __name__ == "__main__":
    add_user_to_whitelist("234821382736")

#the 'demopage.asp' prints all HTTP Headers

