"""
MIT License

Copyright (c) 2021 TheVenomXD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from os import remove
from os import system as execute

from pyrogram import filters
from pyrogram.types import Message

from Suzune import MONGO_URL, SUDOERS, app


@app.on_message(
    filters.command("backup") & filters.user(SUDOERS) & filters.private
)
async def backup(_, message: Message):
    m = await message.reply("Backing up data...")

    code = execute(f'mongodump --uri "{MONGO_URL}"')
    if int(code) != 0:
        return await m.edit(
            "Looks like you don't have mongo-database-tools installed "
            + "grab it from mongodb.com/try/download/database-tools"
        )

    code = execute("zip backup.zip -r9 dump/*")
    if int(code) != 0:
        return await m.edit(
            "Looks like you don't have `zip` package installed, BACKUP FAILED!"
        )

    await message.reply_document("backup.zip")
    await m.delete()
    remove("backup.zip")
