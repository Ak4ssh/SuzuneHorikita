import os
import asyncio
import subprocess
from pyrogram import Client, filters
from src import pbot

# Define a filter to handle messages that reply to a video or GIF
@filters.video | filters.animation
def replied_media_filter(client, update):
    if update.message.reply_to_message and update.message.reply_to_message.video or update.message.reply_to_message.animation:
        return True
    return False

# Define a command to apply the distortion effect
@pbot.on_message(filters.command("distort"))
async def distort_video_or_gif(client, message):
    # Get the replied media file
    media = message.reply_to_message.video or message.reply_to_message.animation
    file_id = media.file_id

    # Download the media file
    file_path = await pbot.download_media(file_id)

    # Define the output file path
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file_path = f"{file_name}_distorted.mp4"

    # Run the distortion command using ffmpeg
    command = f"ffmpeg -i {file_path} -vf 'scale=w=-2:h=-2, zoompan=z='if(eq(zoom,1),1.5,max(1.001,zoom-0.0015))':d=125' -c:a copy {output_file_path}"
    process = await asyncio.create_subprocess_shell(command)
    await process.communicate()

    # Upload the distorted file
    await pbot.send_video(message.chat.id, video=output_file_path)

    # Delete the local files
    os.remove(file_path)
    os.remove(output_file_path)

# Register the filter with Pyrogram
pbot.filter(replied_media_filter)
