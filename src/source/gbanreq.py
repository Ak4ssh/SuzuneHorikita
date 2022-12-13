from datetime import datetime

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
)

import src.source.sql.global_bans_sql as sql
from src import pbot as Client
from src import (
    DEVS,
    Owner as owner_id,
    OWNER_USERNAME as owner_usn,
    SUPPORT_CHAT as log,
)
from src.utils.errors import capture_err


async def user_and_reason(RiZoeL, message):
   args = ("".join(message.text.split(maxsplit=1)[1:])).split(" ", 2)
   if len(args) > 0:
      try:
         user = await RiZoeL.get_users(args[0])
      except Exception as error:
         await message.reply_text(str(error))
         return
      reason = args[1]
      if not reason:
         await message.reply_text("Gime reason!")
         return
   elif message.reply_to_message:
      try:
         user = await RiZoeL.get_users(message.reply_to_message.from_user.id)
      except Exception as error:
         user = message.reply_to_message.from_user
      reason = args[0]
      if not reason:
         await message.reply_text("Gime reason!")
         return
   else:
      await message.reply_text("You need to specify an user!")
      return

   return user, reason


@Client.on_message(filters.command("gban"))
@capture_err
async def reqgban(_, msg: Message):
    if msg.from_user.id == owner_id or msg.from_user.id in DEVS:
        return 
    if msg.chat.username:
        chat_username = (f"@{msg.chat.username} / `{msg.chat.id}`")
    else:
        chat_username = (f"Private Group / `{msg.chat.id}`")

    user, reason = await user_and_reason(Client, msg)
    req_user_id = msg.from_user.id
    req_user_mention = msg.from_user.mention
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    thumb = "https://telegra.ph/file/f56f6518d9f77262903b8.jpg"
    
    bug_report = f"""
**#GbanReq : ** **@{owner_usn}**

**From User : ** {req_user_mention} ({req_user_id})
**Group : ** **{chat_username}**

**Gban Target : ** {user.mention} ({user.id})
**Reason:** {reason}

**Event Stamp : ** **{datetimes}**"""

    if user.id == owner_id or user.id == 1517994352:
        await msg.reply_text("<b>How can be bot owner requesting gban??</b>")
        return
    else:
        check = sql.is_user_gbanned(user.id)
        if not check:
            await msg.reply_text(
                f"<b>Gban Request sent ✓</b>\n\n User: {user.mention} \n Reason: {reason}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Close", callback_data=f"close_reply")
                        ]
                    ]
                )
            )
            await Client.send_photo(
                log,
                photo=thumb,
                caption=f"{bug_report}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "View Reason", url=f"{msg.link}"),
                            InlineKeyboardButton(
                                "Accept Request", callback_data=f"greq:{req_user_id}:{user}")
                        ],
                        [
                            InlineKeyboardButton(
                                "Close", callback_data="close_send_photo")
                        ]
                    ]
                )
            )
        else:
            await msg.reply_text(
                f"<b>User already in Gbanned list!</b>",
            )
        

@Client.on_callback_query(filters.regex("close_reply"))
async def close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()

@Client.on_callback_query(filters.regex("close_send_photo"))
async def close_send_photo(_, CallbackQuery):
    is_Admin = await Client.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not is_Admin.can_delete_messages:
        return await CallbackQuery.answer(
            "You're not allowed to close this.", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()

@Client.on_callback_query(filters.regex(r'greq'))
async def Greport_callback(Akash: Client, callback: CallbackQuery):
    query = callback.data.split(":")
    chat_id = callback.message.chat.id
    message_id = callback.message.id
    if callback.from_user.id == owner_id or callback.from_user.id == 1517994352:
      req_user_id = int(query[1])
      user = str(query[2])
      logs_msg = f"""
**Gban Request accepted ✓**

__By admin:__ {callback.from_user.mention}
__Request by:__ {req_user_id}
__User:__ {user.mention}
"""
      sql.gban_user(user.id, user.first_name, callback.from_user.id)
      m = await Akash.send_message("SuzuneLogs", logs_msg)
      await Akash.edit_message_text(
                 chat_id=chat_id,
                 message_id=message_id,
                 text=f"**Request accepted by {callback.from_user.mention}! Check [logs](https://t.me/SuzuneLogs/{m.id}",
                 disable_web_page_preview=True,
                 )    
