from pyrogram import Client, filters
from src import pbot as app

@app.on_message(filters.command("botlist"))
def get_bot_list(client, message):
    bot_list = []
    members = client.get_chat_members(message.chat.id)
    for member in members:
        if member.is_bot:
            bot_list.append(member.user.username)
    bot_list = "\n".join(bot_list)
    message.reply_text(f"List of bots in this group:\n{bot_list}")
