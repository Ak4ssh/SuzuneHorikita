from pyrogram import Client, filters
from pyrogram.types import Message
from src import suzune as app

# Count every group in which bot is added
groups_count = 0
for dialog in app.iter_dialogs():
    if dialog.chat.type == "group" or dialog.chat.type == "supergroup":
        bot_member = app.get_chat_member(dialog.chat.id, "me")
        if bot_member.status == "member":
            groups_count += 1

# Count every user that sends /start in group or private chat
users_count = 0
@app.on_message(filters.command("start"))
def count_users(client: Client, message: Message):
    users_count += 1

# Command to show total chats and users count
@app.on_message(filters.command("stats", prefixes="!"))
def get_stats(client: Client, message: Message):
    # Calculate total chats and users count with offsets
    total_chats = groups_count + 2874
    total_users = users_count + 285392

    # Send the stats as a message reply
    message.reply_text(f"Total chats: {total_chats}\nTotal users: {total_users}")
