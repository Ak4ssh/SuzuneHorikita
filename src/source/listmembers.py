from pyrogram import Client, filters
import csv
from src import pbot as app

# Define the command to trigger the member listing
@app.on_message(filters.command(["listmembers"]))
def list_members(client, message):
    
    # Get the chat ID of the current chat
    chat_id = message.chat.id
    
    # If the command was sent in a group, get the chat members
    if message.chat.type == "group" or message.chat.type == "supergroup":
        members = client.get_chat_members(chat_id)
    
    # If the command included a group username, get the chat members of that group
    elif len(message.command) > 1:
        username = message.command[1]
        chat = client.get_chat(username)
        members = client.get_chat_members(chat.id)
        
    # If the command was not sent in a group and no group username was provided, return an error message
    else:
        message.reply_text("This command can only be used in a group or with a group username")
        return
    
    # Write the member data to a CSV file named members.txt
    with open("members.txt", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User ID", "First Name", "Last Name", "Username"])
        for member in members:
            writer.writerow([member.user.id, member.user.first_name, member.user.last_name, member.user.username])

    # Reply to the user with the file
    message.reply_document(document="members.txt", caption="Here is the list of members.")
    
