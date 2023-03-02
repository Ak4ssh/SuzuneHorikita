from telethon import TelegramClient, events, sync
from src import ubot2 as client
# define the command filter and the admin filter
command_filter = events.Filters.command(['delete_user_messages'])
admin_filter = events.Filters.user(is_admin=True)

# define the function to delete the user's messages and send the number of deleted messages
async def delete_user_messages(event):
    # check if the user is an admin
    if not await event.is_admin():
        return
    # get the replied message
    reply_msg = await event.get_reply_message()
    # check if the replied message is a message and has a sender
    if reply_msg and reply_msg.sender:
        # delete all messages of the user in the chat
        user_id = reply_msg.sender_id
        count = 0
        async for message in client.iter_messages(event.chat_id, from_user=user_id):
            await message.delete()
            count += 1
        # send a message with the number of deleted messages
        await event.respond(f"{count} messages deleted from user {user_id}.")

# add the event handlers
@client.on(events.NewMessage(func=lambda e: e.is_reply and e.is_private))
@client.on(events.NewMessage(func=lambda e: e.is_reply and e.is_group))
async def on_reply(event):
    await delete_user_messages(event)
