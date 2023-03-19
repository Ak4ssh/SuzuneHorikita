import telethon
from telethon import TelegramClient, events
from src import telethn as client

# Define function to send a message to the admin in DM
async def send_alert(file_link):
    await client.send_message('ADMIN_USER', f"A non-admin user has sent a media file: {file_link}")

# Define event handler for media messages
@client.on(events.NewMessage(func=lambda e: e.media))
async def handle_media(event):
    # Check if user is an admin
    chat = await event.get_chat()
    user = await event.get_user()
    if not chat.admin_rights and not chat.creator:
        # Get link to media file
        if event.media.document:
            file_link = await event.client.get_messages(chat.id, ids=event.message.id).then(lambda msg: msg.file)
        elif event.media.photo:
            file_link = await event.client.get_messages(chat.id, ids=event.message.id).then(lambda msg: msg.photo)
        elif event.media.audio:
            file_link = await event.client.get_messages(chat.id, ids=event.message.id).then(lambda msg: msg.audio)
        elif event.media.voice:
            file_link = await client.get_messages(chat.id, ids=event.message.id).then(lambda msg: msg.voice)
        else:
            file_link = None

        # Send alert message to admin
        if file_link:
            await send_alert(file_link)
