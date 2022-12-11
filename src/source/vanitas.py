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
from vanitas import User as Antispam

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
from src.source.helper_funcs.chat_status import user_admin, user_admin_no_reply
from src import dispatcher, updater, SUPPORT_CHAT, SYL
from src.source.log_channel import gloggable

v = Antispam()

logging.info("AntiSpam System On")


@user_admin_no_reply
@gloggable
def Antispamrm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_Antispam\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat

        is_Antispam = sql.rem_Antispam(chat.id)
        if is_Antispam:
            is_Antispam = sql.rem_Antispam(chat.id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"Antispam_BAN_DISABLED\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.reply_text(
                "Antispam System Disable by {}".format(
                    mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )
            query.message.delete()

    return ""


@user_admin_no_reply
@gloggable
def Antispamadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_Antispam\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat

        is_Antispam = sql.set_Antispam(chat.id)
        if is_Antispam:
            is_Antispam = sql.set_Antispam(chat.id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"Antispam_BAN_ENABLE\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.reply_text(
                "Antispam System Enable by {}".format(
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
                InlineKeyboardButton(text="Modes", callback_data="enabledisablebutton_Antispam({})"),
                InlineKeyboardButton(text="About", callback_data="about_Antispam({})")]])
    message.reply_video(
        video,
        caption="Welcome To The Antispam Module\n Antispam Is Antispam System",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def vantiasban(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id
    is_Antispam = sql.is_Antispam(chat_id)
    if not is_Antispam:
        set_Antispam = sql.set_Antispam(chat_id)
        if set_Antispam:       
            update.effective_message.reply_text(
                 "Antispam System Enable by {}".format(
                    mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )
    else:
        rm_Antispam = sql.rm_Antispam(chat_id)
        if rm_Antispam:
            update.effective_message.reply_text(
                 "Antispam System Disable by {}".format(
                    mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            ) 

    return ""


@user_admin_no_reply
def enabledisable(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    chat: Optional[Chat] = update.effective_chat
    match = re.match(r"enabledisablebutton_Antispam\((.+?)\)", query.data)
    if match:
        if not sql.is_Antispam(chat.id):
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Disable", callback_data="rm_Antispam({})")]])
            update.effective_message.reply_text(
                "Connection to Antispam System can be turned Disable",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
            query.message.delete()
        else:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Enable", callback_data="add_Antispam({})")]])
            update.effective_message.reply_text(
                "Disconnect to Antispam System can be turned Enable",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
            query.message.delete()

    return ""


def about(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"about_Antispam\((.+?)\)", query.data)
    if match:
        keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Support", url="https://t.me/Antispam_support"
                ),
                InlineKeyboardButton(text="Report", url="https://t.me/Antispamreport"
                ),
                InlineKeyboardButton(text="Log", url="https://t.me/Antispamlogs")
            ]
        ]
    )
        update.effective_message.reply_text(
            "Antispam Is A Telegram Antispam System",
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

    is_Antispam = sql.is_Antispam(chat_id)
    if is_Antispam:
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
                            text="Appeal Chat", url="https://t.me/Antispam_support"
                        ),
                        InlineKeyboardButton(text="Modes", callback_data="enabledisablebutton_Antispam({})"
                        )
                    ]
                ]
            )
            update.effective_message.reply_video(
                alertvideo,
                caption=f"<b>Alert</b>: This User Is Blacklisted\n"
                f"<b>Mode</b>: Enable Modes Using /Antispam Disable mode or Change mode\n"
                f"<b>User ID</b>: <code>{x.user}</code>\n"
                f"<b>Enforcer</b>: <code>{x.enforcer}</code>\n"
                f"<b>Reason</b>: <code>{x.reason}</code>\n"
                f"<b>Report</b>: Using /report feature in @BlueMoonVampireBot bot\n",
                reply_markup=kkn,
                parse_mode=ParseMode.HTML,
            )
        return


AntispamBAN_HANDLER = CommandHandler("Antispamban", Antispamban, run_async=True)
BLUEMOON_HANDLER = CommandHandler("Antispam", bluemoon, run_async=True)
ADD_Antispam_HANDLER = CallbackQueryHandler(Antispamadd, pattern=r"add_Antispam", run_async=True)
ENABLE_HANDLER = CallbackQueryHandler(enabledisable, pattern=r"enabledisablebutton_Antispam", run_async=True)
ABOUT_HANDLER = CallbackQueryHandler(about, pattern=r"about_Antispam", run_async=True)
RM_VAINITAS_HANDLER = CallbackQueryHandler(Antispamrm, pattern=r"rm_Antispam", run_async=True)
BLUEMOON_HANDLERK = MessageHandler(filters=Filters.all & Filters.group, callback=bluemoon_callback)

dispatcher.add_handler(ADD_Antispam_HANDLER)
dispatcher.add_handler(AntispamBAN_HANDLER)
dispatcher.add_handler(ENABLE_HANDLER)
dispatcher.add_handler(ABOUT_HANDLER)
dispatcher.add_handler(BLUEMOON_HANDLER)
dispatcher.add_handler(RM_VAINITAS_HANDLER)
dispatcher.add_handler(BLUEMOON_HANDLERK, group=102)
