import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from src.events import register
from src import telethn as tbot
from telethon.tl import types, functions
from RiZoeLX.functions import update_scanlist


VENOM = "https://telegra.ph/file/7c97605753018dfa4f832.mp4"

RIGHTS = types.ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

@register(pattern=("/start"))
async def awake(event):
  TEXT = f"Heya [{event.sender.first_name}](tg://user?id={event.sender.id}), My name is Suzune Horikita - I'm here to help you manage your groups! Hit /help to find out more about how to use me to my full potential.\n\n"
  TEXT += "Join my [News Channel](t.me/SuzuneSuperbot) to get information on all the latest updates."
  BUTTON = [[Button.url("➕Add Me To Your Group➕", "https://t.me/Suzune_Superbot?startgroup=true"),]]
  await tbot.send_file(event.chat_id, VENOM, caption=TEXT, buttons=BUTTON)   

@tbot.on(events.ChatAction)
async def Red7Scanner(message):
  if message.user_joined or message.added_by:
    user = message.sender_id
    msg = f"""
** Alert ⚠️**
User [{user}](tg://user?id={user}) is officially
Scanned by Team Red7 | Phoenix API ;)
Appeal [Here](https://t.me/Red7WatchSupport)
    """
    SCANLIST = update_scanlist()
    if user in SCANLIST:
      try:
         await tbot(functions.channels.EditBannedRequest(message.chat_id, user, BANNED_RIGHTS))
         await tbot.send_message(message.chat_id, msg, link_preview=False)
      except Exception as eorr:
         print(str(eorr))
