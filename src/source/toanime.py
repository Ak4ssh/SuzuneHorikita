import requests
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from src import pbot as app

# Define a filter to handle group messages
@filters.group
def group_filter(_, __, message: Message):
    return True

# Define a command to enhance the image
@app.on_message(group_filter & filters.command("enhance"))
async def enhance(client, message):
    # Check if the message has a replied photo
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply("❌ Please reply to a photo to enhance it.")
        return

    # Get the photo file ID
    photo_file_id = message.reply_to_message.photo[-1].file_id

    # Download the photo file
    photo_url = await client.download_media(photo_file_id)
    photo_file = open(photo_url, "rb")

    # Send the photo file to the waifu2x API to enhance it
    waifu2x_url = "https://waifu2x.booru.pics/api"
    waifu2x_params = {"url": "file://" + photo_url, "scale": 2, "noise": 1}
    waifu2x_response = requests.get(waifu2x_url, params=waifu2x_params)
    waifu2x_response.raise_for_status()

    # Get the enhanced image as a bytes buffer
    enhanced_image_bytes = BytesIO(waifu2x_response.content)

    # Send the enhanced image as a reply
    await message.reply_photo(
        photo=enhanced_image_bytes,
        caption="Enhanced with waifu2x.",
        reply_to_message_id=message.reply_to_message.message_id,
        disable_notification=True,
    )

    # Close the photo file
    photo_file.close()
