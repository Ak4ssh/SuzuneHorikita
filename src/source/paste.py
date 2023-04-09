import os
import requests
from pyrogram import Client, filters
from src import pbot as app

@app.on_message(filters.private & filters.command("paste"))
async def paste_to_pastebin(client, message):
    if message.reply_to_message and message.reply_to_message.document:
        file_path = await message.reply_to_message.download()
    elif message.document:
        file_path = await message.download()
    else:
        await message.reply_text("Please reply to a file or send a file to paste it.")
        return

    with open(file_path, "rb") as f:
        content = f.read()

    data = {
        "api_dev_key": "FBElmQTUl0d86mjn2JEXcG1sCzJ-MJ0O",
        "api_option": "paste",
        "api_paste_code": content.decode("utf-8"),
    }

    response = requests.post("https://pastebin.com/api/api_post.php", data=data)
    os.remove(file_path)

    await message.reply_text(f"Paste URL: {response.text}")

app.run()
