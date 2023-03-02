from pyrogram import Client, filters
from pyrogram.types import User
from src import suzune as app

@app.on_message(filters.command("info") & filters.private)
async def userinfo_command_handler(client, message):
    # get the user ID, username, or replied message
    user_input = message.text.split(" ")[1]
    
    # try to get user information
    try:
        # check if the input is a user ID
        if user_input.isdigit():
            user = await client.get_users(int(user_input))
        # check if the input is a username
        elif user_input.startswith("@"):
            user = await client.get_users(user_input[1:])
        # check if the input is a replied message
        elif message.reply_to_message and message.reply_to_message.from_user:
            user = message.reply_to_message.from_user
        # if none of the above, show an error message
        else:
            await message.reply_text("Invalid input")
            return
    
        # show user information
        await message.reply_text(f"User Info:\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nUser ID: {user.id}\nPermalink: https://t.me/c/{user.id}/{message.message_id}")
        
    # if user is not found, show an error message
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")
        
app.run()
