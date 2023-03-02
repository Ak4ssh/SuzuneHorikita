from pyrogram import Client, filters
from src import suzune as app

# Define a command handler to ban a user
@app.on_message(filters.command("ban", prefixes="/"))
def ban_user(client, message):
    # Check if the user is an admin
    if not message.from_user.is_admin:
        message.reply_text("You must be an admin to use this command.")
        return
    
    # Check if a user was replied to
    if message.reply_to_message and message.reply_to_message.from_user:
        # Ban the replied user
        client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        message.reply_text("User has been banned.")
    else:
        # Check if a username/user ID was given in the command
        if len(message.command) == 2:
            username_or_id = message.command[1]
            try:
                user_id = int(username_or_id)
            except ValueError:
                # If it's not a valid user ID, assume it's a username
                user = client.get_users(username_or_id)
                if user:
                    user_id = user.id
                else:
                    message.reply_text("User not found.")
                    return
            # Ban the user by ID
            client.kick_chat_member(message.chat.id, user_id)
            message.reply_text("User has been banned.")
        else:
            message.reply_text("Please specify a user to ban.")


# Define a command handler to unban a user
@app.on_message(filters.command("unban", prefixes="/"))
def unban_user(client, message):
    # Check if the user is an admin
    if not message.from_user.is_admin:
        message.reply_text("You must be an admin to use this command.")
        return
    
    # Check if a user was replied to
    if message.reply_to_message and message.reply_to_message.from_user:
        # Unban the replied user
        client.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        message.reply_text("User has been unbanned.")
    else:
        # Check if a username/user ID was given in the command
        if len(message.command) == 2:
            username_or_id = message.command[1]
            try:
                user_id = int(username_or_id)
            except ValueError:
                # If it's not a valid user ID, assume it's a username
                user = client.get_users(username_or_id)
                if user:
                    user_id = user.id
                else:
                    message.reply_text("User not found.")
                    return
            # Unban the user by ID
            client.unban_chat_member(message.chat.id, user_id)
            message.reply_text("User has been unbanned.")
        else:
            message.reply_text("Please specify a user to unban.")
            
# Define a command handler to promote a user
@app.on_message(filters.command("promote", prefixes="/"))
def promote_user(client, message):
    # Check if the user is an admin
    if not message.from_user.is_admin:
        message.reply_text("You must be an admin to use this command.")
        return
    
    # Check if a user was replied to
    if message.reply_to_message and message.reply_to_message.from_user:
        # Promote the replied user
        client.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        message.reply_text("User has been promoted.")
    else:
        # Check if a username/user ID was given in the command
        if len(message.command) == 2:
            username_or_id = message.command[1]
            try:
                user_id = int(username_or_id)
            except ValueError:
                # If it's not a valid user ID, assume it's a username
                user = client.get_users(username_or_id)
                if user:
                    user_id = user.id
                else:
                    message.reply_text("User not found.")
                    return
            # Promote the user by ID
            client.promote_chat_member(message.chat.id, user_id)
            message.reply_text("User has been promoted.")
        else:
            message.reply_text("Please specify a user to promote.")

# Define a command handler to demote a user
@app.on_message(filters.command("demote", prefixes="/"))
def demote_user(client, message):
    # Check if the user is an admin
    if not message.from_user.is_admin:
        message.reply_text("You must be an admin to use this command.")
        return
    
    # Check if a user was replied to
    if message.reply_to_message and message.reply_to_message.from_user:
        # Demote the replied user
        client.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions())
        message.reply_text("User has been demoted.")
    else:
        # Check if a username/user ID was given in the command
        if len(message.command) == 2:
            username_or_id = message.command[1]
            try:
                user_id = int(username_or_id)
            except ValueError:
                # If it's not a valid user ID, assume it's a username
                user = client.get_users(username_or_id)
                if user:
                    user_id = user.id
                else:
                    message.reply_text("User not found.")
                    return
            # Demote the user by ID
            client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
            message.reply_text("User has been demoted.")
        else:
            message.reply_text("Please specify a user to demote.")

# Define a function to handle the /setdescription command
@app.on_message(filters.command("setdesc", prefixes="/") & filters.group)
def set_description(client, message):
    # Check if the user is an admin or creator of the group
    if message.from_user.id in (message.chat.creator.id, *message.chat.administrators):
        # If the user is an admin or creator, check if a message is replied to
        if message.reply_to_message:
            # If a message is replied to, set the group description to the text of the message
            description = message.reply_to_message.text
            client.set_chat_description(chat_id=message.chat.id, description=description)
            message.reply_text("Group description updated.")
        elif len(message.command) > 1:
            # If no message is replied to but text is given in the command, set the group description to the text
            description = " ".join(message.command[1:])
            client.set_chat_description(chat_id=message.chat.id, description=description)
            message.reply_text("Group description updated.")
        else:
            # If no message is replied to and no text is given in the command, send an error message
            message.reply_text("Please reply to a message or provide text to set as the group description.")
    else:
        # If the user is not an admin or creator, send an error message
        message.reply_text("You must be an admin or creator of the group to use this command.")

# Define a function to handle the /setgrouppic command
@app.on_message(filters.command("setgpic", prefixes="/") & filters.group)
def set_group_pic(client, message):
    # Check if the user is an admin or creator of the group
    if message.from_user.id in (message.chat.creator.id, *message.chat.administrators):
        # If the user is an admin or creator, check if a photo is replied to
        if message.reply_to_message and message.reply_to_message.photo:
            # If a photo is replied to, set the group profile picture to the photo
            photo = message.reply_to_message.photo[-1]
            client.set_chat_photo(chat_id=message.chat.id, photo=photo.file_id)
            message.reply_text("Group profile picture updated.")
        else:
            # If no photo is replied to, send an error message
            message.reply_text("Please reply to a photo to set as the group profile picture.")
    else:
        # If the user is not an admin or creator, send an error message
        message.reply_text("You must be an admin or creator of the group to use this command.")

# Define a function to handle the /deletegrouppic command
@app.on_message(filters.command("delgpic", prefixes="/") & filters.group)
def delete_group_pic(client, message):
    # Check if the user is an admin or creator of the group
    if message.from_user.id in (message.chat.creator.id, *message.chat.administrators):
        # If the user is an admin or creator, delete the group profile picture
        client.delete_chat_photo(chat_id=message.chat.id)
        message.reply_text("Group profile picture deleted.")
    else:
        # If the user is not an admin or creator, send an error message
        message.reply_text("You must be an admin or creator of the group to use this command.")

# Define a function to handle the /pin command
@app.on_message(filters.command("pin", prefixes="/") & filters.group)
def pin_message(client, message):
    # Check if the user is an admin or creator of the group
    if message.from_user.id in (message.chat.creator.id, *message.chat.administrators):
        # If the user is an admin or creator, check if a message is replied to
        if message.reply_to_message:
            # If a message is replied to, pin the message
            message.reply_to_message.pin()
            message.reply_text("Message pinned.")
        else:
            # If no message is replied to, send an error message
            message.reply_text("Please reply to a message to pin it.")
    else:
        # If the user is not an admin or creator, send an error message
        message.reply_text("You must be an admin or creator of the group to use this command.")

# Define a function to handle the /unpin command
@app.on_message(filters.command("unpin", prefixes="/") & filters.group)
def unpin_message(client, message):
    # Check if the user is an admin or creator of the group
    if message.from_user.id in (message.chat.creator.id, *message.chat.administrators):
        # If the user is an admin or creator, check if a message is replied to
        if message.reply_to_message:
            # If a message is replied to, unpin the message
            message.reply_to_message.unpin()
            message.reply_text("Message unpinned.")
        else:
            # If no message is replied to, unpin the last message
            message.unpin()
            message.reply_text("Last message unpinned.")
    else:
        # If the user is not an admin or creator, send an error message
        message.reply_text("You must be an admin or creator of the group to use this command.")

# Define a function to handle the /unpinall command
@app.on_message(filters.command("unpinall", prefixes="/") & filters.group)
def unpin_all_messages(client, message):
    # Check if the user is an admin or creator of the group
    if message.from_user.id in (message.chat.creator.id, *message.chat.administrators):
        # If the user is an admin or creator, unpin all messages
        client.unpin_all_chat_messages(chat_id=message.chat.id)
        message.reply_text("All messages unpinned.")
    else:
        # If the user is not an admin or creator, send an error message
        message.reply_text("You must be an admin or creator of the group to use this command.")

# Define a function to handle the /refreshadmins command
@app.on_message(filters.command("admincache", prefixes="/") & filters.group)
def refresh_admins(client, message):
    # Check if the user is an admin or creator of the group
    if message.from_user.id in (message.chat.creator.id, *message.chat.administrators):
        # If the user is an admin or creator, get the updated list of administrators
        client.get_chat_members(chat_id=message.chat.id, filter="administrators")
        message.reply_text("Admin list refreshed.")
    else:
        # If the user is not an admin or creator, send an error message
        message.reply_text("You must be an admin or creator of the group to use this command.")

# Define a function to handle the /listadmins command
@app.on_message(filters.command("adminlist", prefixes="/") & filters.group)
def list_admins(client, message):
    # Get the list of administrators for the group
    admins = client.get_chat_members(chat_id=message.chat.id, filter="administrators")
    # Format the list of administrators as a string
    admins_list = "\n".join(f"{admin.user.first_name} ({admin.user.id})" for admin in admins)
    # Send the list of administrators as a message
    message.reply_text(f"List of admins:\n\n{admins_list}")

# Define a function to handle the /listbots command
@app.on_message(filters.command("botlist", prefixes="/") & filters.group)
def list_bots(client, message):
    # Get the list of members for the group
    members = client.get_chat_members(chat_id=message.chat.id)
    # Filter the list of members to only include bots
    bots = [member.user for member in members if member.user.is_bot]
    # Format the list of bots as a string
    bots_list = "\n".join(f"{bot.first_name} ({bot.id})" for bot in bots)
    # Send the list of bots as a message
    message.reply_text(f"List of bots:\n\n{bots_list}")

@app.on_message(filters.regex("@admins") & filters.group)
async def alert_admins_group(client, message):
    # Get the list of administrators for the chat
    admins = await client.get_chat_members(chat_id=message.chat.id, filter="administrators")
    # Send an alert message to all admins in the group chat
    for admin in admins:
        await client.send_message(chat_id=admin.user.id, text=f"{message.from_user.first_name} mentioned '@admins' in {message.chat.title}.")
