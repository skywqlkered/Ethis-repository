import requests
 # which should be followed by uuid or mcname
def get_uuid(mcname:str) -> str | bool:
    
    lookup_url = "https://playerdb.co/api/player/minecraft/"
    """Fetches the uuid of a minecraft account based on the username

    Args:
        mcname (str): the mc username

    Returns:
        str | bool: either the uuid or False if the api status code isnt 200
    """
    response = requests.get(lookup_url + mcname)
    code = response.status_code
    if code != 200:
        return False
    else:
        content = response.json()
        return content["data"]["player"]["id"]
        
def get_username(uuid):
    """Fetches the uuid of a minecraft account based on the username

    Args:
        mcname (str): the mc username

    Returns:
        str | bool: either the uuid or False if the api status code isnt 200
    """
    lookup_url = "https://sessionserver.mojang.com/session/minecraft/profile/"
    response = requests.get(lookup_url + uuid)
    code = response.status_code
    if code != 200:
        return False
    else:
        content = response.json()
        return content["name"]
