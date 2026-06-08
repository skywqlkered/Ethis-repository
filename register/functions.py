import json
import requests
import shutil

registry_path = "./register/registry.json"

def get_json_item(item: str, identifier: str | int) -> dict | None:
    with open(registry_path, "r") as file:
        registry = json.load(file)
        if item == "mc_username" and isinstance(identifier, str):
            for object in registry["users"]:
                if object[item].lower() == identifier.lower():
                    return object
            else:
                return None
            
        else:    
            
            for object in registry["users"]:
                if object[item] == identifier:
                    return object
            else:
                return None

def check_entry(entry: dict) -> list[bool]:
    items = ["discord_id", "mc_uuid", "mc_username"]
    ids = list(entry.values())
    bools = [True if get_json_item(items[i], ids[i]) else False for i in range(3)]
    return bools

def edit_entry(discord_id, uuid, username) -> tuple[dict, dict] | None:
    old_entry = get_json_item("discord_id", discord_id)
    if not old_entry:
        return    
        
    with open(registry_path, "r") as f:
        data = json.load(f)
        data["users"].remove(old_entry)
    
    new_entry = {'discord_id': discord_id, 'mc_uuid': uuid, 'mc_username': username}
    data["users"].append(new_entry)
    
    with open(registry_path, "w") as f:
        json_str = json.dumps(data, indent=4)
        f.write(json_str)
    
    return (old_entry, new_entry)        


def add_entry(discord_id, uuid, username):
    with open(registry_path, "r") as f:
        data = json.load(f)
        entry = {'discord_id': discord_id, 'mc_uuid': uuid, 'mc_username': username}
        data["users"].append(entry)
        
    with open(registry_path, "w") as f:
        json_str = json.dumps(data, indent=4)
        f.write(json_str)
    
    return entry

def remove_entry(discord_id):
    entry = get_json_item("discord_id", discord_id)
    if not entry:
        return    
        
    with open(registry_path, "r") as f:
        data = json.load(f)
        data["users"].remove(entry)
    
    with open(registry_path, "w") as f:
        json_str = json.dumps(data, indent=4)
        f.write(json_str)
    
    return entry
        
def backup_registry():
    shutil.copyfile(registry_path, f"{registry_path[:-5]}_backup.json")
        
def get_uuid(mc_name) -> str | None:    
    lookup_url = "https://playerdb.co/api/player/minecraft/"
    """Fetches the uuid of a minecraft account based on the username

    Args:
        mcname (str): the mc username

    Returns:
        str | None: either the uuid or None if the api status code isnt 200
    """
    response = requests.get(lookup_url + mc_name)
    code = response.status_code
    if code != 200:
        return None
    else:
        content = response.json()
        return content["data"]["player"]["id"]

def get_username(uuid):
    """Fetches the username of a minecraft account based on the uuid

    Args:
        uuid (str): The players uuid

    Returns:
        str | None: either the username or None if the api status code isnt 200
    """
    lookup_url = "https://sessionserver.mojang.com/session/minecraft/profile/"
    response = requests.get(lookup_url + uuid)
    code = response.status_code
    if code != 200:
        return False
    else:
        content = response.json()
        return content["name"]

a = get_json_item("discord_id", 398769543482179585)
b = get_json_item("mc_username", "skywalkered")

# print(add_entry("monkey", 1, 1))

# print(add_entry(1, 1, 1))
# print(check_entry({'discord_id': 1, 'mc_uuid': 23, 'mc_username': 2}))
backup_registry()