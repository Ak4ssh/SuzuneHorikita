import requests
from pyrogram import Client, filters
from src import pbot as app

# Define the command to send and pin the latest anime news
@app.on_message(filters.command("animenews") & filters.group & filters.user(app.get_me().id) & filters.group_admin)
async def send_and_pin_latest_anime(client, message):

    # Send a request to the Anime News Network website
    response = requests.get("https://www.animenewsnetwork.com/")

    # If the request was successful, parse the HTML and extract the latest anime news
    if response.status_code == 200:
        html = response.text
        latest_anime = "Latest anime news from Anime News Network:\n\n"
        for i in range(5):
            start_index = html.find('<div class="herald">')
            end_index = html.find('</div>', start_index)
            news_item = html[start_index:end_index]
            latest_anime += f"{i+1}. {news_item}\n\n"
            html = html[end_index:]

        # Send the latest anime news to the group
        message = await app.send_message(message.chat.id, latest_anime)

        # Pin the latest anime news message to the group
        await app.pin_chat_message(chat_id=message.chat.id, message_id=message.message_id)

    # If the request was not successful, send an error message to the group
    else:
        await message.reply_text("Sorry, there was an error retrieving the latest anime news. Please try again later.")

