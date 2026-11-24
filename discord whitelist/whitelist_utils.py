import json
import os
import sys

import paramiko
from dotenv import load_dotenv

load_dotenv()

HOSTNAME = os.getenv("FTP_HOST")
USERNAME = os.getenv("FTP_USERNAME")
PASSWORD = os.getenv("FTP_PASSWORD")

if not HOSTNAME or not USERNAME or not PASSWORD:
    raise ValueError("FTP credentials are not defined.")

class Whitelist:

    def __init__(self):
        try:
            transport = paramiko.Transport((HOSTNAME, 2022)) #type:ignore
            transport.connect(username=USERNAME, password=PASSWORD) # type:ignore
            sftp = paramiko.SFTPClient.from_transport(transport)

            if not sftp:
                return

            # example: list remote directory
            whitelist_file = sftp.open("whitelist.json")
            data = json.load(whitelist_file)

            sftp.close()
            transport.close()
            
            self.members: dict = data
        
        except Exception as e:  # noqa: BLE001
            print("connection failed:", e)

        if not self.members:
            raise SystemError("Whitelist data could not be extracted")
    
    @property
    def usernames(self):
        return [user_tup["name"] for user_tup in self.members]
    
    @property
    def uuids(self):
        return [user_tup["uuid"] for user_tup in self.members]
        