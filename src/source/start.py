import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from src.events import register
from src import telethn as tbot

VENOM = "https://telegra.ph/file/e3cd9302d6c371593c50d.mp4"

@register(pattern=("/start"))
async def awake(event):
  TEXT = f"Heya [{event.sender.first_name}](tg://user?id={event.sender.id}), My name is Miku - I'm here to help you manage your groups! Hit /help to find out more about how to use me to my full potential.\n\n"
  TEXT += "Join my [News Channel](t.me/astorbots) to get information on all the latest updates."
  BUTTON = [[Button.url("➕Add Me To Your Group➕", "https://t.me/mikuprorobot?startgroup=true"),]]
  await tbot.send_file(event.chat_id, VENOM, caption=TEXT, buttons=BUTTON)
