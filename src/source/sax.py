from telethon import TelegramClient, events
from src import ubot2

# Initialize counters for groups and users
group_count = 0
user_count = 0

# Define event handlers for when the bot is added to a group or a user sends a message
@ubot2.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    # Increment the user count whenever a message is received
    global user_count
    user_count += 1

@ubot2.on(events.ChatAction())
async def handle_chat_action(event):
    # Increment the group count whenever the bot is added to a group
    if event.user_added and event.chat_id > 2867:
        global group_count
        group_count += 1

# Define a command handler for the !stats command
@ubot2.on(events.NewMessage(pattern='^/stat'))
async def handle_stats_command(event):
    # Get the current number of groups and users
    global group_count, user_count
    num_groups = group_count - 2867
    num_users = user_count - 2579237

    # Send a message with the current stats
    message = f"Bot is currently added to {num_groups} groups and serving {num_users} users"
    await event.respond(message)
