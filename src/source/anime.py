import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src import suzune as app

MAL_API_URL = "https://api.jikan.moe/v3"

@app.on_message(filters.command(["anime"]))
def search_anime(client, message):
    query = message.text.split(" ", 1)[1]
    response = requests.get(f"{MAL_API_URL}/search/anime?q={query}&page=1")
    if response.status_code == 200:
        data = response.json()
        if data["result"]:
            anime = data["results"][0]
            anime_photo_url = anime["image_url"]
            anime_title = anime["title"]
            anime_rating = anime["score"]
            anime_description = anime["synopsis"]
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Read More", url=anime["url"])]])
            message.reply_photo(photo=anime_photo_url, caption=f"<b>{anime_title}</b>\n\n"
                                                                  f"<b>Rating:</b> {anime_rating}/10\n\n"
                                                                  f"<b>Description:</b> {anime_description}",
                                  reply_markup=reply_markup,
                                  parse_mode="html")
        else:
            message.reply_text("Sorry, no anime found with that name.")
    else:
        message.reply_text("Something went wrong. Please try again later.")
