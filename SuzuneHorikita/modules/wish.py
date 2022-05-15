from random import choice 
import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from SuzuneHorikita.events import register
from SuzuneHorikita import telethn as tbot

wish = [
    "3", 
    "6", 
    "9", 
    "12", 
    "15", 
    "18", 
    "21", 
    "24", 
    "27", 
    "30",
    "33",
    "36", 
    "35",
    "39", 
    "42", 
    "45", 
    "48", 
    "51", 
    "52",
    "54", 
    "57", 
    "60", 
    "63", 
    "66", 
    "69", 
    "72", 
    "75",
    "78", 
    "81", 
    "83",
    "84", 
    "87", 
    "90", 
    "93", 
    "95",
    "96", 
    "99",
    "100",
]
    

    
@register(pattern=("/wish"))
async def awake(event):
    rem = choice(wish)
        TEXT = f"Your wish has been cast.✨\n\nchance of success: {rem}%  "
        await tbot.send_file(event.chat_id, caption=TEXT)

