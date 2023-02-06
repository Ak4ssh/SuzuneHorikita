import time
from pyrogram import Client, Filters
from src.events import register

banned_users = {}

@register.on_message(Filters.group)
def ban_check(client, message):
    if message.from_user and message.new_chat_members:
        user_id = message.from_user.id
        chat_id = message.chat.id

        if user_id not in banned_users:
            banned_users[user_id] = []
        
        banned_users[user_id].append(time.time())
        
        if len(banned_users[user_id]) >= 5:
            time_diff = banned_users[user_id][-1] - banned_users[user_id][0]
            
            if time_diff <= 5:
                try:
                    client.promote_chat_member(chat_id, user_id, can_change_info=False, can_post_messages=False, can_edit_messages=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=True, can_pin_messages=False, can_promote_members=False)
                except Exception as e:
                    message.reply("I couldn't demote the user because I don't have the necessary permissions.")
                    admins = client.get_chat_administrators(chat_id)
                    admin_ids = [admin.user.id for admin in admins]
                    for admin_id in admin_ids:
                        client.send_message(admin_id, "Please keep an eye on the user that just banned 5 users in 5 seconds, they might be abusing their power.")
            
            banned_users[user_id].clear()
