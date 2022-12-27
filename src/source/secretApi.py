import requests
import urllib
import asyncio
import os
from pyrogram import filters
from src import TEMP_DOWNLOAD_DIRECTORY, pbot as app


@app.on_message(filters.command("tumharimummykechuche"))
async def boobs(client, message):
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    pic_loc = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "bobs.jpg")
    a = await message.reply_text("**chuche loading**")
    await asyncio.sleep(0.5)
    await a.edit("`chuche loading...`")
    nsfw = requests.get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve("http://media.oboobs.ru/{}".format(nsfw), pic_loc)
    await client.send_photo(
        message.chat.id, pic_loc, caption="**😳😋🤤**"
    )
    os.remove(pic_loc)
    await a.delete()
