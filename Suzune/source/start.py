from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo

@Client.on_message(filters.command("start"))
def start_command(client, message):
    video = "https://telegra.ph/file/7c97605753018dfa4f832.mp4"
    TEXT = f"Heya [{client.sender.first_name}](tg://user?id={client.sender.id}), My name is Suzune Horikita - I'm here to help you manage your groups! Hit /help to find out more about how to use me to my full potential.\n\n"
    TEXT += "Join my [News Channel](t.me/SuzuneSuperbot) to get information on all the latest updates."
    keyboard = [[InlineKeyboardButton("Add me to your group", url=f"https://telegram.me/{client.get_me().username}?startgroup=true")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_video(client.chat_id, video=video, caption=TEXT, reply_markup=reply_markup)

