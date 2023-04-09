from pyrogram import Client, filters
import zipfile
import io
from src import pbot as app 

# Zip the replied file
@app.on_message(filters.command("zip") & filters.reply)
def zip_file(client, message):
    reply = message.reply_to_message
    if reply.document:
        with io.BytesIO() as file_bytes:
            file_id = reply.document.file_id
            file_name = reply.document.file_name
            file = client.download_media(file_id)
            with zipfile.ZipFile(file_bytes, mode='w') as zipped:
                zipped.writestr(file_name, file)
            file_bytes.seek(0)
            message.reply_document(file_bytes.getvalue(), f"{file_name}.zip")
    else:
        message.reply_text("Please reply to a file to zip.")

# Unzip the replied file
@app.on_message(filters.command("unzip") & filters.reply)
def unzip_file(client, message):
    reply = message.reply_to_message
    if reply.document:
        with io.BytesIO() as file_bytes:
            file_id = reply.document.file_id
            file_name = reply.document.file_name
            file = client.download_media(file_id)
            with zipfile.ZipFile(io.BytesIO(file)) as zipped:
                file_list = zipped.namelist()
                if len(file_list) > 1:
                    message.reply_text("Zip file contains multiple files. Cannot unzip.")
                    return
                file_bytes.write(zipped.read(file_list[0]))
            file_bytes.seek(0)
            message.reply_document(file_bytes.getvalue(), file_list[0])
    else:
        message.reply_text("Please reply to a zip file to unzip.")
   
