import os

from pyrogram import filters
from pyrogram.types import Message

from src import pbot as pgram



async def get_chat_info(chat, already=False):
    if not already:
        chat = await pgram.get_chat(chat)
    chat_id = chat.id
    username = chat.username
    title = chat.title
    type_ = chat.type
    is_scam = chat.is_scam
    desc = chat.description
    members = chat.members_count
    is_restricted = chat.is_restricted
    if username:
        usn = chat.username
        link = f"[Link](t.me/{username})"
    else:
        usn = "`Null`"
        link = "`Null`"
    dc_id = chat.dc_id
    if chat.photo:
        photo_id = chat.photo.big_file_id
    else:
        return
    body = f"""
.  :Chat Info:  .
ID: `{chat_id}`
DC: `{dc_id}`
Type: `{type_}`
Name: `{title}`
Username: `{usn}`
Mention: `{link}`
Members: `{members}`
Scam: `{is_scam}`
Restricted: `{is_restricted}`
Description: ```{desc}
```
"""
    return [body, photo_id]



@pgram.on_message(filters.command("ginfo"))
async def chat_info_func(_, message: Message):
    try:
        if len(message.command) > 2:
            return await message.reply_text(
                "**Usage:**/ginfo [USERNAME|ID]"
            )

        if len(message.command) == 1:
            chat = message.chat.id
        elif len(message.command) == 2:
            chat = message.text.split(None, 1)[1]

        m = await message.reply_text("Processing")
        

        #info_caption, photo_id = await get_chat_info(chat)
        info_caption, photo_id = await get_chat_info(chat)
        if photo_id == None:
            return await m.edit(info_caption, disable_web_page_preview=True)
        else:
            photo = await pgram.download_media(photo_id)
            await message.reply_photo(photo, caption=info_caption, quote=False)
            await m.delete()
        os.remove(photo)
    except Exception as e:
        await m.edit(e)
