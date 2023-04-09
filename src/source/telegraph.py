import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from src import pbot as app 

# Function to upload media to telegraph and get the generated URL
def upload_to_telegraph(media):
    endpoint = 'https://telegra.ph/upload'
    files = {'file': media}
    r = requests.post(endpoint, files=files)
    return r.json()[0]['url']

# Handler for the command /telegraph
@app.on_message(filters.command('tgm') & filters.reply)
async def telegraph_handler(client: Client, message: Message):
    # Check if the replied message has any media (photo or video)
    if message.reply_to_message.photo or message.reply_to_message.video:
        # Download the media file and upload it to Telegraph
        media = await client.download_media(message.reply_to_message)
        link = upload_to_telegraph(media)
        await message.reply_text(f"Telegraph Link: {link}")
    # If the replied message has text, simply upload it to Telegraph
    elif message.reply_to_message.text:
        text = message.reply_to_message.text
        files = {'text': text}
        r = requests.post('https://api.telegra.ph/createPage', data=files)
        link = 'https://telegra.ph/{}'.format(r.json()['result']['path'])
        await message.reply_text(f"Telegraph Link: {link}")
    else:
        await message.reply_text("Sorry, I can only upload photos, videos or text to Telegraph.")
