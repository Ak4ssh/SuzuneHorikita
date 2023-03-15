import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from src import pbot as app

PASTE_BIN_API_KEY = "d_7U4cLo2nHK056m2Sci82c7z78WFMXg"
PASTE_BIN_URL = "https://pastebin.com/api/api_post.php"

@app.on_message(filters.command(["paste"]))
async def paste_to_pastebin(client: Client, message: Message):
    # check if there is a replied message or file
    if message.reply_to_message:
        text = ""
        if message.reply_to_message.text:
            # if the replied message is text
            text = message.reply_to_message.text
        elif message.reply_to_message.document:
            # if the replied message is a file, get the text
            document = message.reply_to_message.document
            file_id = document.file_id
            file_path = await client.download_media(document=file_id)
            with open(file_path, "r") as f:
                text = f.read()
            os.remove(file_path)
        if text:
            # send the text to Pastebin and get the URL
            data = {
                "api_dev_key": PASTE_BIN_API_KEY,
                "api_option": "paste",
                "api_paste_code": text
            }
            response = requests.post(PASTE_BIN_URL, data=data)
            pastebin_url = response.text
            # send the photo of the full text
            await message.reply_photo(
                photo=f"https://chart.googleapis.com/chart?cht=tx&chl={pastebin_url}",
                caption=f"Full text: {pastebin_url}"
            )
        else:
            await message.reply_text("Sorry, I couldn't get the text.")
    else:
        await message.reply_text("Please reply to a message or file to get the")
