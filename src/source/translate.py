from pyrogram import Client, filters
from pyrogram.types import Message

from googletrans import Translator
from src import suzune as app

# Command to translate the replied message
@app.on_message(filters.command("tr", prefixes="/"))
def translate_message(client: Client, message: Message):
    # Get the target language from the command
    target_lang = message.text.split()[1]

    # Get the replied message to translate
    replied_message = message.reply_to_message
    if not replied_message:
        message.reply_text("Please reply to a message to translate.")
        return

    # Translate the replied message to the target language
    translator = Translator()
    translated_text = translator.translate(replied_message.text, dest=target_lang).text

    # Send the translated text as a message
    message.reply_text(translated_text)
