import asyncio
import os
import sys
import time

from dotenv import load_dotenv
from pyrogram import Client, filters


if os.path.exists(".env"):
    load_dotenv(".env")
  
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", None)

suzune = Client(
    'Suzune',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'Suzune.source'},
)
