from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
from Suzune import app

async def send_video(bot, update):
    caption = f"Heya {update.from_user.first_name}, My name is Suzune Horikita - I'm here to help you manage your groups! Hit /help to find out more about how to use me to my full potential.\n\nJoin my [News Channel](http://t.me/SuzuneSuperbot) to get information on all the latest updates."

    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add me in your group", url="http://t.me/SuzuneSuperbot?startgroup=new")],
    ])

    await bot.send_video(
        chat_id=update.chat.id,
        video="https://graph.org/file/1f2a07be0b1bc76f75fe3.mp4",
        caption=caption,
        reply_markup=inline_keyboard,
        parse_mode="Markdown",
        supports_streaming=True,
    )

@app.on_message(filters.command("start"))
async def start_command(bot, update):
    await send_video(bot, update)
