
import os
import re
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from src.source.sql import global_bans_sql
from telethon import Button, custom, events, functions
from src import telethn as Suzune
from src.events import register
from src import Owner
from src import DEVS as Devs
from telethon.tl.types import (
    Channel,
    DocumentAttributeAudio,
    MessageMediaDocument,
    PhotoEmpty,
    User,
)
from telethon.tl import types
     

async def get_user(event):
    try:
        args = event.text.split(" ", 1)[1].split(" ", 1)
    except IndexError:
        args = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
    elif args:
        user = args[0]
        if user.isnumeric():
            user = int(user)

        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await event.reply("Looks like I don't have control over that user, or the ID isn't a valid one. If you reply to one of their messages, I'll be able to interact with them.")
            return
    elif not args:
       #self_user = await event.get_sender()
       user = event.sender_id
       try:
            user_obj = await event.client.get_entity(user)
       except (TypeError, ValueError):
            await event.reply("Looks like I don't have control over that user, or the ID isn't a valid one. If you reply to one of their messages, I'll be able to interact with them.")
            return

    else:
        await event.reply("I don't know who you're talking about, you're going to need to specify a user...!")
        return
    return user_obj

@register(pattern=("/info"))
async def _info(e):
    event = e
    x_user = await get_user(event)

    if isinstance(x_user, User):
        x_full = await e.client(GetFullUserRequest(x_user.username or x_user.id))
        out_str = "<b>User Info:</b>"
        out_str += f"\n<b>First Name:</b> {x_user.first_name}"
        if x_user.last_name:
            out_str += f"\n<b>Last Name:</b> {x_user.last_name}"
        if x_user.username:
            out_str += f"\n<b>Username:</b> @{x_user.username}"
        out_str += f"\n<b>User ID:</b> <code>{x_user.id}</code>"
        out_str += (f"\n<b>PermaLink:</b> <a href='tg://user?id={x_user.id}'>link</a>")
        if int(x_user.id) in Owner:
            out_str += f"\n\n <b> Owner Of Suzune 🔱 </b>"
        if int(x_user.id) in Devs:
            out_str += "\n\n<b>Dev Of Suzune</b>"
        if gban_sql.is_gbanned(x_user.id):
            out_str += "\n\n<b>Globally Banned:</b> Yes"
        try:
           await e.reply(out_str, file=x_full.user.profile_photo, parse_mode="html")
        except:
           await e.reply(out_str, parse_mode="html")
    if isinstance(x_user, Channel):
        x_channel = await e.client(GetFullChannelRequest(x_user.username or x_user.id))
        out_str = f"<b>Channel Info:</b>"
        out_str += f"\n<b>Title:</b> {x_user.title}"
        if x_user.username:
            out_str += f"\n<b>Username:</b> @{x_user.username}"
        out_str += f"\n<b>Chat ID:</b> <code>{x_user.id}</code>"
        if x_user.verified:
            out_str += "\n<b>Verified:</b> True"
        if x_channel.full_chat.about:
            out_str += f"\n\n<b>Description:</b> <code>{x_channel.full_chat.about}</code>"
        if len(x_channel.chats) == 2:
            out_str += f"\n<b>Linked Chat:</b> {x_channel.chats[1].title}"
            out_str += (
                f"\n<b>Linked Chat ID:</b> <code>-100{x_channel.chats[1].id}</code>"
            )
        if x_channel.full_chat.admins_count:
           out_str += f"\n<b>Admins:</b> <code>{x_channel.full_chat.admins_count}"
        file = x_channel.full_chat.chat_photo
        if isinstance(file, PhotoEmpty):
            file = None
        await e.reply(out_str, file=file, parse_mode="html")
