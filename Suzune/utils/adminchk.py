from Suzune import app
from pyrogram.types import Message
import asyncio


async def admin_check(c: app, m: Message):
    chat_id = m.chat.id
    user_id = m.from_user.id

    check_status = await c.get_chat_member(chat_id=chat_id, user_id=user_id)
    admin_strings = ["creator", "administrator"]
    if check_status.status not in admin_strings:
        await m.reply_text("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await m.delete()
        return False

    return True

async def extract_user(message: Message) -> (int, str):
    """extracts the user from a message"""
    user_id = None
    user_first_name = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name
