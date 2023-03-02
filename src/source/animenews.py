import jikanpy
from pyrogram import Client, filters
from pyrogram.types import Message
from src import pbot as app

# Initialize the Jikan API client
jikan = jikanpy.Jikan()

# Define a filter to handle group messages
@filters.group
def group_filter(_, __, message: Message):
    return True

# Define a command to fetch the latest news for an anime
@app.on_message(group_filter & filters.command("animenews") & filters.chat_admin)
async def anime_news(client, message):
    # Get the anime name from the command arguments
    anime_name = " ".join(message.command[1:])

    # Search for the anime and get its ID
    anime_search_results = jikan.search("anime", anime_name)
    if not anime_search_results.get("results"):
        await message.reply("❌ Anime not found.")
        return

    anime_id = anime_search_results["results"][0]["mal_id"]

    # Fetch the latest news for the anime
    anime = jikan.anime(anime_id)
    news = anime.get("news", [])

    if not news:
        await message.reply("📰 No news found for this anime.")
        return

    # Get the anime picture
    picture_url = anime["image_url"]

    # Format the news as a message
    title = anime.get("title")
    news_items = "\n\n".join([f"{n['url']} - {n['title']}" for n in news])
    news_message = f"📰 Latest news for {title}:\n\n{news_items}"

    # Post the news message with the anime's picture
    news_message = await client.send_photo(
        chat_id=message.chat.id,
        photo=picture_url,
        caption=news_message,
        disable_notification=True,
    )

    # Pin the news message
    await news_message.pin()
