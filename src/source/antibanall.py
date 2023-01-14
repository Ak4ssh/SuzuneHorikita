import html
from typing import Optional

from telegram import ParseMode, Update
from telegram.chatmemberupdated import ChatMemberUpdated
from telegram.ext import CallbackContext
from telegram.ext.chatmemberhandler import ChatMemberHandler
from src.source.sql import antibanall_sql as sql

def extract_status_change(chat_member_update: ChatMemberUpdated):
    try:
        status_change = chat_member_update.difference().get("status")
    except AttributeError:  # no change in status
        status_change = None

    try:
        title_change = chat_member_update.difference().get("custom_title")
    except AttributeError:  # no change in title
        title_change = None

    return status_change, title_change


def do_ban(chat):  # announce to chat or only to log channel?
    return bool(chat.type != "chat" and sql.active(chat.id))


@loggable
def antiban(update: Update, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    chat = update.effective_chat
    message = update.effective_message
    oldstat = str(status.split(",")[0])
    status = ",".join(status_change)
    newstat = str(status.split(",")[1])
    result = extract_status_change(update.chat_member)
    status_change, title_change = result

    if (
        title_change is not None and status_change is None
    ):  # extract title changes for admins
        oldtitle, newtitle = title_change
        member_name = update.chat_member.new_chat_member.user.mention_html()
        if oldtitle != newtitle:
        
           if oldstat != "kicked" and newstat == "kicked":
              if do_ban(chat):
              checker = sql.get_bans(chat.id, user.id)
              if not checker:
                return
              bot.promoteChatMember(
                    chat.id,
                    user_id,
                    can_change_info=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_voice_chats=False,
                    )
              bot.sendMessage(
                    chat.id,
                    f"<b> Anti banall active in this chat! I'm demoting to user {member_name}",
                    parse_mode=ParseMode.HTML,
                    )

NEKO_PTB.add_handler(
    ChatMemberHandler(antiban, ChatMemberHandler.CHAT_MEMBER, run_async=True)
)

""" Used Pyrogram """

import re
from pyrogram import filters
from pyrogram.types import Message
from src import pbot
from pyrogram import enums

async def owner_check(_, __, msg: Message):
    """if user is Owner or not."""
    if msg.from_user.id in [1517994352, 1789859817]:
        return True

    user = await m.chat.get_member(m.from_user.id)

    if user.status == enums.ChatMemberStatus.OWNER:
        status = True
    else:
        status = False
        if user.status == enums.ChatMemberStatus.ADMINISTRATOR:
            reply_ = "You're an admin only, stay in your limits!"
        else:
            reply_ = "Do you think that you can execute owner commands?"
        await mag.reply_text(reply_)

    return status

owner_only = filters.create(owner_check)

@pbot.on_message(filters.group & owner_only & filters.command(["antibanall"))
async def antibanall(RiZoeL: pbot, message: Message):
    user = message.from_user
    chat = message.chat
    if user.id != [1517994352, 1789859817]:
       return
    if user.id
    try:
       args = message.text.split(" ", 1)[1].split(" ", 1)
    except IndexError:
       args = None
    if args:
       txt = str(args[0]):
       if re.search("on|yes".lower(), txt.lower()):
         sql.add(chat.id)
         await message.reply_text(f"Anti-banall actived in {chat.title}")
         return
       elif re.search("off|of|no".lower(), txt.lower()): 
         sql.remove(chat.id)
         await message.reply_text(f"Anti-banall de-actived in {chat.title}")
         return
       else:
         await message.reply_text("**Wrong Usage!** \n\nsyntax: /antibanall on/off")
         return
    else:
       active = sql.active(chat.id)
       if active:
          await message.reply_text("Anti-Banall is actived in this chat!")
       else:
          await message.reply_text("Anti-Banall id not actived in this chat!")
