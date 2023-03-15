import asyncio
from telethon import TelegramClient, events, sync
import feedparser
from src import telethn as client

# Set up the group chat where you want to send the daily news and pin it.

chat_id = -1001511742995
sudo_user_ids = [6185365707, 1517994352]
# Set up the RSS feed URL for the news source you want to use.
rss_feed_url = 'http://feeds.bbci.co.uk/news/rss.xml'

# Define a function to send the news to the group chat.
async def send_news():
    # Parse the RSS feed to get the latest news.
    feed = feedparser.parse(rss_feed_url)
    latest_news = feed.entries[0]
    news_title = latest_news.title
    news_link = latest_news.link
    news_description = latest_news.description

    # Send the news to the group chat.
    await client.send_message(chat_id, f'{news_title}\n{news_link}\n{news_description}')

    # Pin the news message to the top of the chat.
    global news_message_id
    news_message = await client.get_messages(chat_id, limit=1)
    news_message_id = news_message[0].id
    await client.pin_message(chat_id, news_message_id)

# Define an event handler to send the news when an admin sends the /daily_news command.
@client.on(events.NewMessage(pattern='/news'))
async def send_daily_news(event):
    if event.sender_id in sudo_user_ids:
        await send_news()

