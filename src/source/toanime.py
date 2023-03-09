import os
import subprocess
from pyrogram import Client, filters
from src import pbot as app

# Define the command to enhance replied photos
@app.on_message(filters.command("enhance") & filters.reply & filters.photo & filters.private)
async def enhance_photo(client, message):

    # Get the photo file ID and download the photo
    photo_file_id = message.reply_to_message.photo.file_id
    photo_file = await client.download_media(photo_file_id)

    # Run waifu2x-caffe on the downloaded photo file
    subprocess.run(["waifu2x-caffe-cui.exe", "-i", photo_file, "-o", photo_file + "_enhanced.png"])

    # Send the enhanced photo as a message to the chat
    await client.send_photo(chat_id=message.chat.id, photo=photo_file + "_enhanced.png")

    # Delete the downloaded and enhanced photo files
    os.remove(photo_file)
    os.remove(photo_file + "_enhanced.png")
