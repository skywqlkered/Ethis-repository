import ftplib
import os
import sys
import socket

from dotenv import load_dotenv

load_dotenv()

# Fill Required Information
HOSTNAME = os.getenv("FTP_HOST")
USERNAME = os.getenv("FTP_USERNAME")
PASSWORD = os.getenv("FTP_PASSWORD")

if not HOSTNAME or not USERNAME or not PASSWORD:
    raise ValueError("FTP credentials are not defined.")




x = socket.getaddrinfo(HOSTNAME, 2022)