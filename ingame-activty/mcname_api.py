import requests

lookup_url = "https://playerdb.co/api/player/minecraft/" # which should be followed by uuid or mcname
def get_uuid(mcname:str) -> str | bool:
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
        
