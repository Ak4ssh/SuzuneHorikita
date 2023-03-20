import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from src.events import register
from src import telethn as tbot


VENOM = "https://telegra.ph/file/7c97605753018dfa4f832.mp4"

@register(pattern=("/start"))
async def awake(event):
  TEXT = f"Heya [{event.sender.first_name}](tg://user?id={event.sender.id}), My name is Suzune Horikita - I'm here to help you manage your groups! Hit /help to find out more about how to use me to my full potential.\n\n"
  TEXT += "Join my [News Channel](t.me/SuzuneSuperbot) to get information on all the latest updates."
  BUTTON = [[Button.url("➕Add Me To Your Group➕", "https://t.me/Suzune_Superbot?startgroup=true"),]]
  await tbot.send_file(event.chat_id, VENOM, caption=TEXT, buttons=BUTTON)   
