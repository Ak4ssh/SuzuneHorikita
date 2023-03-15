from src.events import register
from src import telethn as tbot
from telethon import events

@register.on(events.NewMessage(pattern='/paste'))
async def paste_to_pastebin(event):
    # check if there is a replied message or file
    if event.is_reply and event.reply_to_msg_id:
        replied_msg = await event.get_reply_message()
        text = ''
        if replied_msg.text:
            # if the replied message is text
            text = replied_msg.text
        elif replied_msg.media:
            # if the replied message is a file, get the text
            media = replied_msg.media
            file_path = await client.download_media(media, file=os.path.join(os.getcwd(), 'downloads'))
            with open(file_path, 'r') as f:
                text = f.read()
            os.remove(file_path)
        if text:
            # send the text to Pastebin and get the URL
            data = {
                'api_dev_key': PASTEBIN_API_KEY,
                'api_option': 'paste',
                'api_paste_code': text
            }
            response = requests.post(PASTEBIN_URL, data=data)
            pastebin_url = response.text
            # send the photo of the full text
            await tbot.send_file(
                event.chat_id,
                file=f'https://chart.googleapis.com/chart?cht=tx&chl={pastebin_url}',
                caption=f'Full text: {pastebin_url}'
            )
        else:
            await event.reply('Sorry, I couldn\'t get the text.')
    else:
        await event.reply('Please reply to a message or file to get the text.')
