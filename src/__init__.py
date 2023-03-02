import asyncio
import os
import sys
import time

from dotenv import load_dotenv
from pyrogram import Client, filters
from pytgcalls import PyTgCalls


if os.path.exists(".env"):
    load_dotenv(".env")

# -------------CONFIGS--------------------
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", None)


def make_int(str_input):
    str_list = str_input.split(" ")
    int_list = []
    for x in str_list:
        int_list.append(int(x))
    return int_list


sudo = os.getenv("SUDO_USERS")
SUDO_USERS = []
if sudo:
    SUDO_USERS = make_int(sudo)
DEVS = [1517994352, 6185365707, 1432756163]
for x in DEVS:
    SUDO_USERS.append(x)

#----------------------------------------------

suzune = Client(
    'Suzune',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'src.source'},
)
