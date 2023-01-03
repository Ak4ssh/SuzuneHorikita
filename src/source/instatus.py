import asyncio
from datetime import datetime
from pyrogram import enums , filters 
from src import pbot as pgram

COMMANDERS = [enums.ChatMemberStatus.ADMINISTRATOR,enums.ChatMemberStatus.OWNER]

@pgram.on_message(filters.command(["instatus"]) & ~filters.private)
async def instatus(_, message):    
    chat_id = message.chat.id
    user_id = message.from_user.id
    start = datetime.now()
    user = await pgram.get_chat_member(chat_id,user_id)
    count = await pgram.get_chat_members_count(chat_id)
    text = await message.reply("ɢᴇᴛᴛɪɴɢ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜɪs ᴄʜᴀᴛ.......")
    if user.status in COMMANDERS:       
        recently = 0
        within_week = 0
        within_month = 0
        long_time_ago = 0
        deleted_acc = 0
        premium_acc = 0
        no_username = 0
        restricted = 0
        banned = 0        
        bot = 0
        async for ban in pgram.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            banned += 1
        async for restr in pgram.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED):
            restricted += 1
        async for member in pgram.get_chat_members(chat_id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.is_premium:
                premium_acc += 1
            elif not user.username:
                no_username += 1
            elif user.status.value == "recently":
                recently += 1
            elif user.status.value == "last_week":
                within_week += 1
            elif user.status.value == "last_month":
                within_month += 1
            elif user.status.value == "long_ago":
                long_time_ago += 1
            else:
                pass
        
        time = (datetime.now() - start).seconds
        await text.edit(f"""
        ⧃ {message.chat.title}
——————«•»——————
🎎 ɢʀᴏᴜᴘ ɪɴғᴏ

👥 ᴍᴇᴍʙᴇʀs » {str(count)} 

🎣 ᴄʜᴀᴛ ᴛʏᴘᴇ » {message.chat.type}

⚡ᴄʜᴀᴛ ɪᴅ » `{message.chat.id}`

💌 ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ » @{message.chat.username}
——————«•»——————
👁‍🗨 ᴍᴇᴍʙᴇʀs's sᴛᴀᴛᴜs

🕜 ʀᴇᴄᴇɴᴛʟʏ » {recently}

🕰️ ʟᴀsᴛ ᴡᴇᴇᴋ » {within_week}

⏱️ ʟᴀsᴛ ᴍᴏɴᴛʜ » {within_month}

⌛ ʟᴏɴɢ ᴀɢᴏ » {long_time_ago}

🙄 ᴡɪᴛʜᴏᴜᴛ ᴜsᴇʀɴᴀᴍᴇ » {no_username}
🤐 ʀᴇsᴛʀɪᴄᴛᴇᴅ » {restricted}
🚫 ʙʟᴏᴄᴋᴇᴅ » {banned}
👻 ᴅᴇʟᴇᴛᴇᴅ » {deleted_acc}
🤖 ʙᴏᴛs » {bot}
⭐️ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs : {premium_acc}
——————«•»——————

⏱ ᴛɪᴍᴇ ᴛᴏᴏᴋ » {time} sᴇᴄᴏɴᴅs
""")
 
    else:
        await text.edit("You must be an admin or group owner to perform this action.")
        await asyncio.sleep(5)
