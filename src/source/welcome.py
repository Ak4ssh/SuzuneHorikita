from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import os
from src import suzune as app

welcome_enabled = False

# Define the function that will send the anime welcome video with the user's name
def send_welcome_video(chat_id, first_name):
    url = "https://api.danbot.xyz/text/yt_comment?comment="
    comment = f"Welcome to the group, {first_name}! Enjoy your stay!"
    url += comment.replace(" ", "+")
    response = requests.get(url)
    if response.status_code == 200:
        response_json = response.json()
        if response_json["success"]:
            video_url = response_json["video"]
            video_file = requests.get(video_url)
            with open("welcome_video.mp4", "wb") as f:
                f.write(video_file.content)
            app.send_video(chat_id, "welcome_video.mp4", caption=comment)
            os.remove("welcome_video.mp4")

# Define the command handler to turn on and off the welcome feature
@app.on_message(filters.command("welcome") & filters.user([YOUR_ADMIN_IDS]))
def welcome_command_handler(client: Client, message: Message):
    global welcome_enabled
    if len(message.command) > 1:
        if message.command[1].lower() == "on":
            welcome_enabled = True
            message.reply("Welcome message enabled!")
        elif message.command[1].lower() == "off":
            welcome_enabled = False
            message.reply("Welcome message disabled!")
    else:
        message.reply("Please specify 'on' or 'off' to enable/disable welcome messages.")

# Define the handler to send the welcome message when a new member joins
@app.on_chat_member_updated()
def welcome_message_handler(client: Client, message: Message):
    global welcome_enabled
    if welcome_enabled and message.new_chat_members:
        chat_id = message.chat.id
        first_name = message.new_chat_members[0].first_name
        send_welcome_video(chat_id, first_name)
