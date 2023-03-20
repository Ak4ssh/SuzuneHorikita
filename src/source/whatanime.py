from telethon import TelegramClient, events
import requests
import io
from PIL import Image
from src import telethn as client

# Define a function to handle incoming messages
@client.on(events.NewMessage(pattern='/whatanime'))
async def whatanime(event):
    # Check if the message has a reply
    if not event.reply_to_msg_id:
        await event.reply('Please reply to a photo or gif to use this command.')
        return

    # Get the message being replied to
    reply = await event.get_reply_message()

    # Check if the replied message is a photo or gif
    if not reply.photo and not reply.gif:
        await event.reply('Please reply to a photo or gif to use this command.')
        return

    # Get the largest available photo or gif
    if reply.photo:
        file = reply.photo[-1]
    else:
        file = reply.gif

    # Download the file
    file_data = await client.download_media(file)

    # Open the file as an image
    image = Image.open(io.BytesIO(file_data))

    # Convert the image to JPEG format
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)

    # Send the image to the whatanime API and get the response
    response = requests.post(
        'https://api.trace.moe/search',
        files={'image': buffer},
        headers={'Content-Type': 'multipart/form-data'}
    ).json()

    # Check if the API was able to recognize the anime
    if response['result']:
        result = response['result'][0]
        await event.reply(f'Title: {result["anilist"]["title"]["romaji"]}\n'
                           f'Episode: {result["episode"]}\n'
                           f'Time: {result["from"]}-{result["to"]}\n'
                           f'Similarity: {result["similarity"]:.2%}\n'
                           f'MAL URL: https://myanimelist.net/anime/{result["anilist"]["id"]}')
    else:
        await event.reply('Sorry, I could not recognize this anime.')
