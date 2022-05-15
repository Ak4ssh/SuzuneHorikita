"""
Copyright (c) 2022 Axel (aksr-aashish)
This is part of @vexanafanclub so don't change anything....
"""

import asyncio
from pyrogram import filters
from SuzuneHorikita import pbot as app
from pyrogram.types import Message
from SuzuneHorikita.utils.errors import capture_err

active_channel = []


async def eor(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


async def channel_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            text = "**ChannelMode` enabled`.**"
            return await eor(message, text=text)
        await eor(message, text="`ChannelMode` Enabled.")
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await eor(message, text=" ChannelMode Disabled!")
        await eor(message, text=f"**ChannelMode Disabled in :- ** {message.chat.id} ❌")
    else:
        await eor(message, text="Error Cant Use this way\n\n1->`/channel on` \n 2->`/channel off`\n\nNote :- Cmds are not case `sensitive`")



@app.on_message(filters.command("channel") & ~filters.edited)
@capture_err
async def channel_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text="Error Cant Use this way\n\n1->`/channel on` \n 2->`/channel off`\n\nNote :- Cmds are not case `sensitive`")
    await channel_toggle(active_channel, message)




@app.on_message(filters.text & ~filters.linked_channel, group=36)        
@app.on_message(filters.media & ~filters.linked_channel, group=36)
@app.on_message(filters.sticker & ~filters.linked_channel, group=36)
@app.on_message(filters.via_bot & ~filters.linked_channel, group=36)
async def anitchnl(_, message):
  chat_id = message.chat.id
  if message.sender_chat:
    sender = message.sender_chat.id 
    if message.chat.id not in active_channel:
        return
    if chat_id == sender:
        return
    else:
        await message.delete()
        ti = await message.reply_text("**Chaneel Mess Deleted! chat id = '{chat_id}**")
        await asyncio.sleep(4)
        await ti.delete()        
