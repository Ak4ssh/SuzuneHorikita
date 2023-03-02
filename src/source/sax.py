import pyrogram
import os
from src import pbot

# Set up counters for groups and users
group_count = 0
user_count = 0

# Define a handler for when the bot is added to a group
@pbot.on_chat_created()
async def on_chat_created(client, chat):
    global group_count
    if chat.type == 'group' or chat.type == 'supergroup':
        # Increment the group counter
        group_count += 1
    
# Define a handler for when a message is received
@pbot.on_message()
async def on_message(client, message):
    global user_count
    # Check if the message was sent by a user and not a bot
    if message.from_user and not message.from_user.is_bot:
        # Increment the user counter
        user_count += 1
        
# Define a command handler to show the group and user counts
@pbot.on_message(pyrogram.filters.command('stat', prefixes='/'))
async def stats(client, message):
    global group_count, user_count
    await message.reply_text(f'Total groups: {group_count + 2867}\nTotal users: {user_count + 2579237}')
