from telethon import TelegramClient, events
from src import telethn as client

# Replace the value below with the chat ID where you want the bot to listen for messages
chat_id = -1001680514362

# Define the event handler function for file/media messages
@client.on(events.NewMessage(chats=chat_id, incoming=True, document=lambda d: d.mime_type.startswith('image/') or d.mime_type.startswith('video/')))
async def handle_new_media(event):
    # Get the media file name and message link
    file_name = event.media.document.attributes[0].file_name
    message_link = f"https://t.me/{event.chat.username}/{event.id}"

    # Get a list of all group admins
    async for admin in client.iter_participants(chat_id, filter='administrators'):
        # Send a message to the admin with the file name and message link
        await client.send_message(admin.id, f"ALERT: {file_name} was sent in {event.chat.title}. Message link: {message_link}")
