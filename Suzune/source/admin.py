from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_filter = filters.create(lambda _, __, message: message.from_user.is_admin)

@Client.on_message(filters.command("ban") & admin_filter)
def ban_user(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        message.reply("Please specify a user to ban.")
        return

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=f"ban_{user_id}"), InlineKeyboardButton("No", callback_data="cancel_ban")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply(f"Are you sure you want to ban user {user_id}?", reply_markup=reply_markup)

@Client.on_callback_query(filters.regex(r"^ban_(\d+)$"))
def confirm_ban(client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    chat_member = client.get_chat_member(chat_id, user_id)
    if not chat_member.is_admin:
        callback_query.answer("You are not an admin.")
        return

    banned_user_id = int(callback_query.matches[0].group(1))
    client.kick_chat_member(chat_id, banned_user_id)
    callback_query.answer("User banned.")

@Client.on_callback_query(filters.regex(r"^cancel_ban$"))
def cancel_ban(client, callback_query):
    callback_query.answer("Ban cancelled.")

