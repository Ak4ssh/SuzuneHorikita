from pyrogram import Client, filters
from pyrogram.types import ChatMember
from src import pbot

@pbot.on_message(filters.command(["botlist"]))
def get_bot_list(client, message):
    # Get the list of members in the chat
    members = client.get_chat_members(message.chat.id)
    
    # Filter the members to include only the bots
    bots = [member.user for member in members if isinstance(member, ChatMember) and member.user.is_bot]
    
    # Send the list of bots as a reply to the message
    bot_names = "\n".join([f"{bot.first_name} (@{bot.username})" for bot in bots])
    message.reply_text(f"List of bots in this group:\n{bot_names}")
