import pyrogram
import os
import requests
import json
from src import pbot
# Set up the OpenAI API credentials
openai_key = os.environ.get('OPENAI_API_KEY')

@pbot.on_message(pyrogram.filters.command('identify', prefixes='/'))
async def identify_character(client, message):
    # Check if the message is a reply to a photo or sticker
    if message.reply_to_message and (message.reply_to_message.photo or message.reply_to_message.sticker):
        # Download the photo or sticker
        file_id = message.reply_to_message.photo.file_id if message.reply_to_message.photo else message.reply_to_message.sticker.file_id
        file_path = await client.download_media(file_id)
        
        # Send a message to indicate that we are processing the image
        await message.reply_text('Processing the image...')
        
        # Use OpenAI to identify the character name
        try:
            url = 'https://api.openai.com/v1/images/gpt-3'
            headers = {'Authorization': f'Bearer {openai_key}'}
            files = {'image': open(file_path, 'rb')}
            response = requests.post(url, headers=headers, files=files)
            response_data = json.loads(response.text)
            output_text = response_data['data'][0]['caption']
            await message.reply_text(f'The character in the image is likely to be {output_text}')
        except Exception as e:
            await message.reply_text(f'An error occurred while processing the image: {e}')
            
    # If the message is not a reply to a photo or sticker, inform the user
    else:
        await message.reply_text('Please reply to a photo or sticker to use this command.')
