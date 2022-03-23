import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from SuzuneHorikita.events import register
from SuzuneHorikita import telethn as tbot


PHOTO = "https://telegra.ph/file/6001b9d2ba6d3c183b979.mp4"

@register(pattern=("/alive"))
async def awake(event):
  TEXT = f"**Hi [{event.sender.first_name}](tg://user?id={event.sender.id}), I'm SuzuneHorikita** \n\n"
  TEXT += "⚪ **I'm Working Properly** \n\n"
  TEXT += f"⚪ **My Master : [𓆩𝐀ᴋ𝐀s𝐇𓆪™](https://t.me/TheVenomXD)** \n\n"
  TEXT += f"⚪ **Library Version :** `{telever}` \n\n"
  TEXT += f"⚪ **Telethon Version :** `{tlhver}` \n\n"
  TEXT += f"⚪ **Pyrogram Version :** `{pyrover}` \n\n"
  TEXT += "**Thanks For Adding Me Here️**"
  BUTTON = [[Button.url("Help", "https://t.me/Suzune_Superbot?start=help"), Button.url("Support", "https://t.me/Suzune_Support")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=TEXT,  buttons=BUTTON)
