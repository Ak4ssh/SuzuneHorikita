from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserAdminInvalid
from Suzune import suzune as app

# define the command to ban a user
@app.on_message(filters.command("ban") & filters.group)
def ban_user(client, message):
    # check if user is an admin
    chat_id = message.chat.id
    user_id = message.from_user.id

    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.status in ["creator", "administrator"]:
        # get the user to ban
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) == 2:
            user_id = message.command[1]
        else:
            message.reply("Usage: /ban (user id) /ban @username /ban (replied user)")
            return

        # ask for confirmation with an inline button
        confirm_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data=f"ban_{user_id}"), InlineKeyboardButton("No", callback_data="cancel")]
        ])
        message.reply(f"Are you sure you want to ban {user_id}?", reply_markup=confirm_markup)
    else:
        message.reply("You must be an admin to use this command.")

# handle inline button callbacks
@app.on_callback_query()
def handle_callback(client, callback_query):
    if callback_query.data.startswith("ban_"):
        # get the user to ban from the callback data
        user_id = int(callback_query.data.split("_")[1])

        # try to ban the user
        try:
            client.kick_chat_member(callback_query.message.chat.id, user_id)
            callback_query.answer("User has been banned.")
        except UserAdminInvalid:
            callback_query.answer("I can't ban that user because they're an admin.")
    elif callback_query.data == "cancel":
        callback_query.answer("Action canceled.")
    else:
        callback_query.answer("Unknown callback data.")
