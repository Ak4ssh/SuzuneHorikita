import logging
import os
import json
import re
import os
import html
import requests
from telegram.ext.filters import Filters
from telegram.parsemode import ParseMode

import src.source.sql.vanitas_sql as sql
from vanitas import User as antispam

from time import sleep
from telegram import ParseMode
from telegram import (CallbackQuery, Chat, MessageEntity, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message, ParseMode, Update, Bot, User)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          DispatcherHandlerStop, Filters, MessageHandler,
                          run_async)
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown

from src.source.helper_funcs.filters import CustomFilters
from src.source.helper_funcs.chat_status import TheRiZoeL, TheRiZoeL_no_reply
from src import dispatcher, updater, SUPPORT_CHAT, SYL
from src.source.log_channel import gloggable

v = antispam()

logging.info("antispam System On")


@TheRiZoeL_no_reply
@gloggable
def antispamrm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_antispam\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat

        is_antispam = sql.rem_antispam(chat.id)
        if is_antispam:
            is_antispam = sql.rem_antispam(chat.id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"antispam_BAN_DISABLED\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.reply_text(
                "antispam System Disable by {}".format(
                    mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )
            query.message.delete()

    return ""


@TheRiZoeL_no_reply
@gloggable
def antispamadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_antispam\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat

        is_antispam = sql.set_antispam(chat.id)
        if is_antispam:
            is_antispam = sql.set_antispam(chat.id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"antispam_BAN_ENABLE\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.reply_text(
                "antispam System Enable by {}".format(
                    mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )
            query.message.delete()

    return ""


def bluemoon(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message
    video = "https://telegra.ph/file/08ee83677137fdf3c70ba.mp4"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Modes", callback_data="enabledisablebutton_antispam({})"),
                InlineKeyboardButton(text="About", callback_data="about_antispam({})")]])
    message.reply_video(
        video,
        caption="Welcome To The antispam Module\n antispam Is antispam System",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def antispamban(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id
    is_antispam = sql.is_antispam(chat_id)
    if not is_antispam:
        set_antispam = sql.set_antispam(chat_id)
        if set_antispam:       
            update.effective_message.reply_text(
                 "antispam System Enable by {}".format(
                    mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )
    else:
        rm_antispam = sql.rm_antispam(chat_id)
        if rm_antispam:
            update.effective_message.reply_text(
                 "antispam System Disable by {}".format(
                    mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            ) 

    return ""


@TheRiZoeL_no_reply
def enabledisable(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    chat: Optional[Chat] = update.effective_chat
    match = re.match(r"enabledisablebutton_antispam\((.+?)\)", query.data)
    if match:
        if not sql.is_antispam(chat.id):
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Disable", callback_data="rm_antispam({})")]])
            update.effective_message.reply_text(
                "Connection to antispam System can be turned Disable",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
            query.message.delete()
        else:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Enable", callback_data="add_antispam({})")]])
            update.effective_message.reply_text(
                "Disconnect to antispam System can be turned Enable",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
            query.message.delete()

    return ""


def about(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"about_antispam\((.+?)\)", query.data)
    if match:
        keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Support", url="https://t.me/antispam_support"
                ),
                InlineKeyboardButton(text="Report", url="https://t.me/antispamreport"
                ),
                InlineKeyboardButton(text="Log", url="https://t.me/antispamlogs")
            ]
        ]
    )
        update.effective_message.reply_text(
            "antispam Is A Telegram antispam System",
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )
        query.message.delete()

    return ""


def bluemoon_callback(update: Update, context: CallbackContext, should_message=True):
    message = update.effective_message
    chat_id = update.effective_chat.id
    chat = update.effective_chat
    user = update.effective_user

    is_antispam = sql.is_antispam(chat_id)
    if is_antispam:
        return
        x = None
    try:
        x = v.get_info(int(user.id))
    except:
        x = None

    if x:
        update.effective_chat.ban_member(x.user)
        update.effective_chat.unban_member(x.user)
        if should_message:
            alertvideo = "https://telegra.ph/file/fed47f651097bb2f5e6ca.mp4"
            kkn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Appeal Chat", url="https://t.me/antispam_support"
                        ),
                        InlineKeyboardButton(text="Modes", callback_data="enabledisablebutton_antispam({})"
                        )
                    ]
                ]
            )
            update.effective_message.reply_video(
                alertvideo,
                caption=f"<b>Alert</b>: This User Is Blacklisted\n"
                f"<b>Mode</b>: Enable Modes Using /antispam Disable mode or Change mode\n"
                f"<b>User ID</b>: <code>{x.user}</code>\n"
                f"<b>Enforcer</b>: <code>{x.enforcer}</code>\n"
                f"<b>Reason</b>: <code>{x.reason}</code>\n"
                f"<b>Report</b>: Using /report feature in @BlueMoonVampireBot bot\n",
                reply_markup=kkn,
                parse_mode=ParseMode.HTML,
            )
        return


antispamBAN_HANDLER = CommandHandler("antispamban", antispamban, run_async=True)
BLUEMOON_HANDLER = CommandHandler("antispam", bluemoon, run_async=True)
ADD_antispam_HANDLER = CallbackQueryHandler(antispamadd, pattern=r"add_antispam", run_async=True)
ENABLE_HANDLER = CallbackQueryHandler(enabledisable, pattern=r"enabledisablebutton_antispam", run_async=True)
ABOUT_HANDLER = CallbackQueryHandler(about, pattern=r"about_antispam", run_async=True)
RM_VAINITAS_HANDLER = CallbackQueryHandler(antispamrm, pattern=r"rm_antispam", run_async=True)
BLUEMOON_HANDLERK = MessageHandler(filters=Filters.all & Filters.group, callback=bluemoon_callback)

dispatcher.add_handler(ADD_antispam_HANDLER)
dispatcher.add_handler(antispamBAN_HANDLER)
dispatcher.add_handler(ENABLE_HANDLER)
dispatcher.add_handler(ABOUT_HANDLER)
dispatcher.add_handler(BLUEMOON_HANDLER)
dispatcher.add_handler(RM_VAINITAS_HANDLER)
dispatcher.add_handler(BLUEMOON_HANDLERK, group=102)
