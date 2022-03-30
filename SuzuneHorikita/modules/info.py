import os

from pyrogram import filters
from pyrogram.types import Message

from SuzuneHorikita import DEV_USERS
from SuzuneHorikita import pbot as app
from SuzuneHorikita.services.sections import section


async def get_user_info(user, already=False):
    if not already:
        user = await app.get_users(user)
    if not user.first_name:
        return ["Deleted account", None]
    user_id = user.id
    username = user.username
    first_name = user.first_name
    mention = user.mention("Link")
    dc_id = user.dc_id
    photo_id = user.photo.big_file_id if user.photo else None
    is_sudo = user_id in DEV_USERS
    is_bot = user.is_bot
    is_fake = user.is_fake
    status = user.status
    if status == "offline":
        last_date = user.last_online_date
    else:
        last_date = "User is currently online"
    mention = user.mention("first_name")
    body = {
        "ID": user_id,
        "DC": dc_id,
        "Name": [first_name],
        "Username": [("@" + username) if username else None],
        "Mention": [mention],
        "Sudo": is_sudo,
        "Bot" : is_bot,
        "Fake" : is_fake,
        "Status" : status
        "Last seen" : last_date
        "Mention" : mention
    }
    caption = section("User info", body)
    return [caption, photo_id]


async def get_chat_info(chat, already=False):
    if not already:
        chat = await app.get_chat(chat)
    chat_id = chat.id
    username = chat.username
    title = chat.title
    type_ = chat.type
    is_scam = chat.is_scam
    is_fake = chat.is_fake
    description = chat.description
    members = chat.members_count
    is_restricted = chat.is_restricted
    link = f"[Link](t.me/{username})" if username else None
    dc_id = chat.dc_id
    photo_id = chat.photo.big_file_id if chat.photo else None
    can_save = chat.has_protected_content
    body = {
        "ID": chat_id,
        "DC": dc_id,
        "Type": type_,
        "Name": [title],
        "Username": [("@" + username) if username else None],
        "Mention": [link],
        "Members": members,
        "Scam": is_scam,
        "Fake" : is_fake,
        "Can save content" : can_save,
        "Restricted": is_restricted,
        "Description": [description],
    }
    caption = section("Chat info", body)
    return [caption, photo_id]


@app.on_message(filters.command("uinfo"))
async def info_func(_, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) == 1:
        user = message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user = message.text.split(None, 1)[1]

    m = await message.reply_text("Processing...")

    try:
        info_caption, photo_id = await get_user_info(user)
    except Exception as e:
        return await m.edit(str(e))

    if not photo_id:
        return await m.edit(
            info_caption, disable_web_page_preview=True
        )
    photo = await app.download_media(photo_id)

    await message.reply_photo(
        photo, caption=info_caption, quote=False
    )
    await m.delete()
    os.remove(photo)


@app.on_message(filters.command("cinfo"))
async def chat_info_func(_, message: Message):
    try:
        if len(message.command) > 2:
            return await message.reply_text(
                "**Usage:**cinfo <chat id/username>"
            )

        if len(message.command) == 1:
            chat = message.chat.id
        elif len(message.command) == 2:
            chat = message.text.split(None, 1)[1]

        m = await message.reply_text("Processing...")

        info_caption, photo_id = await get_chat_info(chat)
        if not photo_id:
            return await m.edit(
                info_caption, disable_web_page_preview=True
            )

        photo = await app.download_media(photo_id)
        await message.reply_photo(
            photo, caption=info_caption, quote=False
        )

        await m.delete()
        os.remove(photo)
    except Exception as e:
        await m.edit(e)


__mod_name__ = "nothing"
