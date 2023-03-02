from telethon import TelegramClient, events
from telethon.errors import PeerIdInvalidError, ChannelPrivateError, ChatAdminRequiredError
from telethon.tl.types import PeerUser, PeerChannel
from telethon.tl.functions.messages import GetHistoryRequest, DeleteMessagesRequest
from src import ubot2 as client

# Get the username of the admin of the group or channel
async def get_admin_username(chat):
    async for user in client.iter_participants(chat):
        if user.status == 'creator' or user.status == 'administrator':
            return user.username

# Define a function to delete all messages of a specific user in a group or channel
async def delete_user_messages(chat, user_id):
    # Get the admin username
    admin_username = await get_admin_username(chat)

    # Check if the user is an admin
    try:
        user = await client.get_entity(user_id)
        if user.username == admin_username:
            await client.send_message(chat, "You cannot delete messages of an admin.")
            return
    except ChatAdminRequiredError:
        await client.send_message(chat, "You cannot delete messages of an admin.")
        return
    except Exception as e:
        await client.send_message(chat, "An error occurred: {}".format(str(e)))
        return

    # Get the chat entity
    try:
        chat_entity = await client.get_entity(chat)
    except (PeerIdInvalidError, ValueError):
        await client.send_message(chat, "Invalid chat or channel.")
        return

    # Get the messages of the user
    messages = []
    async for message in client.iter_messages(chat_entity, from_user=user_id):
        messages.append(message.id)

    # Delete the messages
    if messages:
        await client(DeleteMessagesRequest(chat, messages))
        await client.send_message(chat, "{} messages deleted from user {}.".format(len(messages), user_id))
    else:
        await client.send_message(chat, "No messages found from user {}.".format(user_id))

# Define an event handler for the command
@client.on(events.NewMessage(pattern='/delall'))
async def delete_user(event):
    # Check if the user is an admin
    if event.chat.admin_rights or event.chat.creator:
        # Check if there is a replied user
        if event.is_reply:
            # Get the user ID of the replied message
            user_id = (await event.get_reply_message()).sender_id
            await delete_user_messages(event.chat_id, user_id)
        else:
            await event.reply("Please reply to a user message to delete all messages.")
    else:
        await event.reply("You are not an admin of this group or channel.")
