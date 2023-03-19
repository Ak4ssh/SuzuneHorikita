from pyrogram import Client, filters
import time
from src import pbot as client

chat_id = -1001680514362

@client.on_message(filters.document | filters.video | filters.audio | filters.photo)
def delete_copyrighted_files(client, message):
    message_id = message.message_id
    time.sleep(30)
    client.delete_messages(chat_id, message_id)
