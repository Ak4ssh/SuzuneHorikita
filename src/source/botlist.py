import asyncio
from telethon import TelegramClient, events, sync
from src import telethn as client

# Define a function to get the list of all the bots in the group chat
async def get_bots_list(chat):
    # Get all the members in the group chat
    async for member in client.iter_participants(chat):
        # Check if the member is a bot
        if member.bot:
            # Send the bot's username to the group chat
            await client.send_message(chat, f'🤖 @{member.username}')

# Define an event handler to trigger when an admin sends the /bots command
@client.on(events.NewMessage(pattern='/bots', from_users='admin'))
async def handler(event):
    # Get the chat where the command was sent
    chat = await event.get_chat()

    # Get the list of all the bots in the group chat
    await get_bots_list(chat)
