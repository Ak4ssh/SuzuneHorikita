import pyrogram
import requests
import io
import pytesseract
import re
from src import pbot

# Define function to get character name from image using OCR
def get_character_name(image_url):
    # Download image and read text using OCR
    image_data = requests.get(image_url).content
    text = pytesseract.image_to_string(io.BytesIO(image_data), lang='eng')
    
    # Extract possible character names from text using regular expressions
    character_names = re.findall(r'[A-Z][a-z]+\s?[A-Z][a-z]+', text)
    
    # Return the first character name found, if any
    if character_names:
        return character_names[0]
    else:
        return None

# Define callback function to handle messages
@pbot.on_message()
def handle_message(client, message):
    # Check if message is a command and a reply to a photo or sticker
    if message.text and message.text.startswith('/identify') and message.reply_to_message and (message.reply_to_message.photo or message.reply_to_message.sticker):
        # Check if the replied message is a sticker and download it if necessary
        if message.reply_to_message.sticker:
            sticker = message.reply_to_message.sticker
            image_url = f"https://api.telegram.org/file/bot{client.token}/{sticker.file_id}.webp"
        else:
            photo = message.reply_to_message.photo[-1]
            image_url = f"https://api.telegram.org/file/bot{client.token}/{photo.file_id}.jpg"
        # Get the character name using OCR
        character_name = get_character_name(image_url)
        # Reply with the character name
        if character_name:
            message.reply(f"The character in this photo/sticker is {character_name}")
        else:
            message.reply("Could not identify any characters in this photo/sticker")
