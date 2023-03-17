from pyrogram import Client, filters
from pyrogram.types import Message
from src import pbot as app

chat_id = -1001680514362

# Define a function to get the message link for a given message ID
def get_message_link(message_id):
    return f"https://t.me/c/{chat_id}/{message_id}"

# Define a function to handle media messages
@app.on_message(filters.media & filters.group)
def handle_media(bot, message):
    # Get the media file ID and type
    file_id = message.photo[-1].file_id if message.photo else message.video.file_id
    file_type = 'photo' if message.photo else 'video'

    # Get the message link for the current message
    message_link = get_message_link(message.message_id)

    # Get a list of all group admins
    group_admins = bot.get_chat_members(chat_id, filter='administrators')

    # Send an alert message to each admin with the file type and link
    for admin in group_admins:
        bot.send_message(chat_id=admin.user.id, text=f"Alert ⚠️ New {file_type} file was uploaded to the group: {message_link}")

