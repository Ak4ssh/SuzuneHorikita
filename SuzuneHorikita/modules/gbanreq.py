import html
import json
import os
from typing import Optional

from SuzuneHorikita import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    SUPPORT_CHAT,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
from SuzuneHorikita.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    whitelist_plus,
    support_plus,
)
from SuzuneHorikita.modules.helper_funcs.extraction import extract_user
from SuzuneHorikita.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), "SuzuneHorikita/elevated_users.json")


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply

@support_plus
@gloggable
def gbanreq(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    update.effective_message.reply_text(
        rt
        + "\nSuccessfully Sent Your Request".format(
            user_member.first_name,
        ),
    )

    log_message = (
        f"▪︎ GBAN REQUEST\n"
        f"<b>▪︎Requested By:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>▪︎Victim:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



GBANREQ_HANDLER = CommandHandler(("gban", "req"), gbanreq, run_async=True)
dispatcher.add_handler(GBANREQ_HANDLER)
