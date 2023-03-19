import asyncio
import time
from telethon import TelegramClient, events, sync
import feedparser
from src import telethn as client
from newsapi import NewsApiClient
# Set up the group chat where you want to send the daily news and pin it.

chat_id = -1001511742995
ak4sh = 6185365707
sudo_user_ids = [6185365707, 1517994352]
# Set up the RSS feed URL for the news source you want to use.
rss_feed_url = 'http://rss.cnn.com/rss/edition_world.rss'

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
        
        
newsapi = NewsApiClient(api_key='bfd09c7fd4694ac18676fab9291d36a4')

# Define function to retrieve news articles from Kolkata
def get_kolkata_news():
    top_headlines = newsapi.get_top_headlines(q='Kolkata')
    articles = top_headlines['articles']
    return articles

# Define function to send news articles to user on Telegram
async def send_kolkata_news():
    # Get latest news articles
    articles = get_kolkata_news()

    # Send each article to user
    for article in articles:
        message = f"{article['title']}\n{article['description']}\n{article['url']}"
        await client.send_message(ak4sh, message)

# Define function to set up daily schedule
async def daily_news():
    while True:
        # Get current time
        now = time.localtime()

        # Check if it's time to send news articles
        if now.tm_hour == 8 and now.tm_min == 0:
            await send_kolkata_news()

        # Wait 1 minute before checking again
        time.sleep(60)
