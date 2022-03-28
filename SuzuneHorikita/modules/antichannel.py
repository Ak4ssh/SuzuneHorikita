"""
Copyright (c) 2021 Itzz-axel
This is part of @VexanaFAnClub so don't change anything....
"""

import asyncio
from pyrogram import filters
from SuzuneHorikita import pbot as app
from pyrogram.types import Message
from SuzuneHorikita import eor
from SuzuneHorikita.utils.errors import capture_err

active_channel = []






async def channel_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            text = "**ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ᴇɴᴀʙʟᴇ ✅. I will delete all message that send with channel names in {message.chat.id} .**"
            return await eor(message, text=text)
        await eor(message, text="ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ᴇɴᴀʙʟᴇ .")
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await eor(message, text="ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ᴅɪsᴀʙʟᴇ!")
        await eor(message, text=f"**ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜᴇ ᴄʜᴀᴛt** {message.chat.id} ❌")
    else:
        await eor(message, text="ᴘʟᴇᴀsᴇ ᴜsᴇ `/antichannel on` ᴏʀ  off` ᴏɴʟʏ ")


# Enabled | Disable antichannel


@app.on_message(filters.command("antichannel") & ~filters.edited)
@capture_err
async def antichannel_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text="ᴘʟᴇᴀsᴇ ᴜsᴇ `/antichannel on` ᴏʀ  off` ᴏɴʟʏ")
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
        ti = await message.reply_text("*ᴄʜᴀɴɴᴇʟ ᴍᴇss ʜᴀs ʙᴇᴇɴ ᴅᴇᴛᴇᴛᴇᴄᴛᴇᴅ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇsғᴜʟʟʏ . **")
        await asyncio.sleep(7)
        await ti.delete()        
        
__help__ = """
*User Commands:*
❂ /antichannel on *:*Toggle anti channel mode 
❂ /antichannel on *:*Disable anti channel mode 

"""

__mod_name__ = "anti channel"        
