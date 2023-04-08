from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
from Suzune import app


@app.on_message(filters.command(["start"]))
async def start_command(client, message):
    video_file_id = "https://graph.org/file/1f2a07be0b1bc76f75fe3.mp4"
    caption = f"Heya {message.from_user.first_name}, My name is Suzune Horikita - I'm here to help you manage your groups! Hit /help to find out more about how to use me to my full potential.\n\nJoin my [News Channel](http://t.me/SuzuneSuperbot) to get information on all the latest updates."
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Add me to your group", url="https://telegram.me/Suzune_Superbot?startgroup=new")]]
    )
    await app.send_video(chat_id=message.chat.id, video=video_file_id, caption=caption, reply_markup=keyboard)

@pbot.on_message(filters.command("play"))
def handle_music(client, message):
    # create an inline keyboard with a button
    button = InlineKeyboardButton(
        "Yurri Music Bot",
        url="https://t.me/YurriMusicBot"
    )
    keyboard = InlineKeyboardMarkup([[button]])

    # send a message with the inline keyboard
    message.reply_text(
        "**Notice**: Due to `FloodWaitError` Music Services Has Been Shifted.\nTap below to be redirected to the music bot.",
        reply_markup=keyboard
    )
