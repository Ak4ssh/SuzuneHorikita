import os
from database import db
from pyrogram import Client, filters
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from logging.handlers import RotatingFileHandler
import html
import time
from datetime import datetime
from io import BytesIO

from telegram import ParseMode, Update
from telegram.error import BadRequest, TelegramError, Unauthorized
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

import SuzuneHorikita.modules.sql.global_bans_sql as sql
from SuzuneHorikita.modules.sql.users_sql import get_user_com_chats
from SuzuneHorikita import (
    DEV_USERS,
    EVENT_LOGS,
    OWNER_ID,
    STRICT_GBAN,
    DRAGONS,
    SUPPORT_CHAT,
    SPAMWATCH_SUPPORT_CHAT,
    DEMONS,
    TIGERS,
    WOLVES,
    sw,
    dispatcher,
)
from SuzuneHorikita.modules.helper_funcs.chat_status import (
    is_user_admin,
    support_plus,
    user_admin,
)
from SuzuneHorikita.modules.helper_funcs.extraction import (
    extract_user,
    extract_user_and_text,
)
from SuzuneHorikita.modules.helper_funcs.misc import send_to_list

user_id, reason = extract_user_and_text(message, args)
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

@dev_plus
@gloggable
def gbanreq(update: Update, context: CallbackContext) -> str:
    update.effective_message.reply_text(
        rt
        + "\nSuccessfully Sent Your Request".format(
            user_member.first_name,
        ),
    )

    log_message = (
        f"▪︎ GBAN REQUEST ▪︎\n"
        f"<b>▪︎Requested By:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>▪︎Victim:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        f"<b>▪︎Reason:</b> <code>{reason}</code>\n"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



GBANREQ_HANDLER = CommandHandler(("gban", "req"), gbanreq, run_async=True)
dispatcher.add_handler(GBANREQ_HANDLER)
