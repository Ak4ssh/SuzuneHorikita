from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (ChatAdminRequired, PeerIdInvalid, RightForbidden,
                             RPCError, UserAdminInvalid)
from src import suzune as app

# define the ban command handler
@app.on_message(filters.command("ban") & filters.group & filters.user("self"))
def ban_user(client, message):
    # check if the user is an admin in the group
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        member = client.get_chat_member(chat_id, user_id)
        if not member.can_restrict_members:
            message.reply_text("Sorry, you are not an admin in this group.")
            return
    except ChatAdminRequired:
        message.reply_text("Sorry, I need to be an admin in this group to execute this command.")
        return
    except RPCError as e:
        message.reply_text(f"Sorry, an error occurred: {e}")
        return

    # check if a user was provided to ban
    if not message.reply_to_message:
        message.reply_text("Please provide a user to ban.")
        return

    # get the user to ban
    user = message.reply_to_message.from_user

    # ban the user
    try:
        client.kick_chat_member(chat_id, user.id)
        message.reply_text(f"{user.username} has been banned from the group.")
    except UserAdminInvalid:
        message.reply_text("Sorry, I cannot ban an admin in this group.")
    except RightForbidden:
        message.reply_text("Sorry, I do not have the necessary rights to ban users in this group.")
    except PeerIdInvalid:
        message.reply_text("Sorry, the user ID is invalid.")
    except RPCError as e:
        message.reply_text(f"Sorry, an error occurred: {e}")
    else:
        message.reply_text(f"{user.username} has been banned from the group.")
