from pyrogram import Client, filters
from pyrogram.types import Message
from src import suzune as app

afk_users = {}

@app.on_message(filters.command("afk", prefixes="/"))
def afk_command_handler(client: Client, message: Message):
    global afk_users
    afk_users[message.chat.id] = message.from_user.id
    message.reply("You are now AFK.")

@app.on_message(filters.mentioned)
def mentioned_handler(client: Client, message: Message):
    global afk_users
    if message.chat.id in afk_users.values():
        for user_id in afk_users:
            if afk_users[user_id] == message.chat.id:
                user = client.get_users(user_id)
                message.reply(f"{user.first_name} is AFK.")

@app.on_message(filters.text & ~filters.private)
def back_online_handler(client: Client, message: Message):
    global afk_users
    if message.from_user.id in afk_users.values() and message.chat.id == message.from_user.id:
        for user_id in afk_users:
            if afk_users[user_id] == message.from_user.id:
                user = client.get_users(user_id)
                message.reply(f"{user.first_name} is back online!")
                del afk_users[user_id]
