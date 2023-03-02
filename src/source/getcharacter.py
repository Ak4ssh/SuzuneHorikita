import pyrogram
import requests
import io
from google.cloud import vision_v1
from google.cloud.vision_v1 import enums
from src import pbot


# Define function to get character name from image using Google Lens
def get_character_name(image_url):
    # Initialize Google Cloud Vision client and API request
    client = vision_v1.ImageAnnotatorClient()
    image = vision_v1.types.Image()
    image.source.image_uri = image_url
    features = [{'type': enums.Feature.Type.OBJECT_LOCALIZATION}]

    # Send API request and extract object annotations
    response = client.annotate_image({'image': image, 'features': features})
    object_annotations = response.localized_object_annotations

    # Extract the object with the highest score and return its name
    highest_score = 0
    character_name = None
    for object in object_annotations:
        if object.score > highest_score and object.name.lower() != "person":
            highest_score = object.score
            character_name = object.name
    return character_name

# Define callback function to handle messages
@pbot.on_message()
def handle_message(client, message):
    # Check if message is a command and a reply to a photo
    if message.text and message.text.startswith('/identify') and message.reply_to_message and message.reply_to_message.photo:
        # Get the largest available photo size
        photo = message.reply_to_message.photo[-1]
        # Download the photo and get its URL
        file_path = client.download_media(photo.file_id)
        image_url = "file://" + file_path
        # Get the character name using Google Lens
        character_name = get_character_name(image_url)
        # Reply with the character name
        if character_name:
            message.reply(f"The character in this photo is {character_name}")
        else:
            message.reply("Could not identify any characters in this photo")
