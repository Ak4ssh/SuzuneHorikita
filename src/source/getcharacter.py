import os
import requests
import telethon
import io
import openai
import re
from src import pbot
# Set up OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define function to get character name from image using OpenAI
def get_character_name(image_url):
    # Download image and create OpenAI API request
    image_data = requests.get(image_url).content
    prompt = f"Identify the character in this image: {image_url}"
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.5)
    
    # Extract possible character names from OpenAI response using regular expressions
    character_names = re.findall(r'[A-Z][a-z]+\s?[A-Z][a-z]+', response.choices[0].text)
    
    # Return the first character name found, if any
    if character_names:
        return character_names[0]
    else:
        return None

# Define command handler function
@pbot.on(telethon.events.NewMessage(pattern="/identify"))
async def handle_command(event):
    # Check if message is a reply to a photo or sticker
    if event.is_reply and (await event.get_reply_message()).photo or (await event.get_reply_message()).sticker:
        # Check if the replied message is a sticker and download it if necessary
        if (await event.get_reply_message()).sticker:
            sticker = await (await event.get_reply_message()).download_media()
            image_url = f"data:image/webp;base64,{sticker}"
        else:
            photo = await (await event.get_reply_message()).download_media()
            image_url = f"data:image/jpeg;base64,{photo}"
        # Get the character name using OpenAI
        character_name = get_character_name(image_url)
        # Reply with the character name
        if character_name:
            await event.reply(f"The character in this photo/sticker is {character_name}")
        else:
            await event.reply("Could not identify any characters in this photo/sticker")
