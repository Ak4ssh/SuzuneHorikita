from pyrogram import Client, filters
import base64
from src import pbot as app

# Define the /encode command
@app.on_message(filters.command("encode"))
def encode(client, message):
    # Get the input string to be encoded
    input_str = message.text.split(" ", 1)[1]
    # Encode the input string using Base64 encoding
    encoded_str = base64.b64encode(input_str.encode("utf-8")).decode("utf-8")
    # Reply to the user with the encoded string
    message.reply_text(f"Base64 Encoded:\n{encoded_str}")

# Define the /decode command
@app.on_message(filters.command("decode"))
def decode(client, message):
    # Get the input string to be decoded
    input_str = message.text.split(" ", 1)[1]
    # Decode the input string using Base64 decoding
    decoded_str = base64.b64decode(input_str.encode("utf-8")).decode("utf-8")
    # Reply to the user with the decoded string
    message.reply_text(f"Base64 Decoded:\n{decoded_str}")
