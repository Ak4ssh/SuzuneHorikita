from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
from src import pbot as app 


@app.on_message(filters.command(["Google"]))
async def google_search(client, message):
    query = message.text.split(" ", 1)[1]
    search_url = f"https://www.google.com/search?q={query}&num=5"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
    output = ""
    for result in results:
        output += result.get_text() + "\n"
    await client.send_message(message.chat.id, output)




@app.on_message(filters.command(["img"]))
async def image_search(client, message):
    query = message.text.split(" ", 1)[1]
    search_url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    image_results = soup.find_all("img", class_="rg_i")
    output = ""
    for i in range(5):
        if i >= len(image_results):
            break
        img_url = image_results[i]["src"]
        output += f"{i + 1}. {img_url}\n"
        await client.send_photo(
            chat_id=message.chat.id,
            photo=img_url,
            caption=f"Image {i + 1} of {len(image_results)}",
        )
    if not output:
        await message.reply_text("No results found.")


@app.on_message(filters.command(["reverse"]))
async def reverse_search(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("Please reply to a photo.")
        return

    photo_url = message.reply_to_message.photo.file_id
    search_url = f"https://www.google.com/searchbyimage?image_url={photo_url}"
    response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    link_tags = soup.find_all("a", class_="iu-card-header")
    output = ""
    for link_tag in link_tags:
        url = link_tag["href"]
        if not url.startswith("/search"):
            output += f"{url}\n"
    if output:
        await message.reply_text(output)
    else:
        await message.reply_text("No similar images found.")


inline = "Search"

saxsux = """
• /google <query>*:* Perform a google search
• /image <query>*:* Search Google for images and returns them\nFor greater no. of results specify lim, For eg: `/img hello lim=10`
• /app <appname>*:* Searches for an app in Play Store and returns its details.
• /reverse: Does a reverse image search of the media which it was replied to.
• /gps <location>*:* Get gps location.
• /github <username>*:* Get information about a GitHub user.
• /country <country name>*:* Gathering info about given country
• /imdb <Movie name>*:* Get full info about a movie with imdb.com
• Suzune <query>*:* Suzune answers the query

  💡Ex: `Suzune where is Japan?`
"""
