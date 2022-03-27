import html

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.filters import Filters
from telegram.ext import CallbackContext, Filters, CommandHandler, run_async, CallbackQueryHandler

from SuzuneHorikita.AntiChannel.anonymous import AdminPerms, user_admin
from SuzuneHorikita.AntiChannel.decorators import shasacmd, shasamsg
from SuzuneHorikita.modules.sql.antichannel_sql import (
    antichannel_status,
    disable_antichannel,
    enable_antichannel,
)

from SuzuneHorikita import (
    DEV_USERS,
    LOGGER,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)

from SuzuneHorikita.modules.log_channel import gloggable, loggable
from SuzuneHorikita.modules.helper_funcs.chat_status import (
    user_admin_no_reply,
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin,
    user_can_ban,
    can_delete,
    dev_plus,
)

@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
@dev_plus
def antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html(
                "Enabled antichannel in {}".format(html.escape(chat.title))
            )
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html(
                "Disabled antichannel in {}".format(html.escape(chat.title))
            )
        else:
            message.reply_text("Unrecognized arguments {}".format(s))
        return
    message.reply_html(
        "Antichannel setting is currently {} in {}".format(
            antichannel_status(chat.id), html.escape(chat.title)
        )
    )
   
def eliminate_channel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    if (
        message.sender_chat
        and message.sender_chat.type == "channel"
        and not message.is_automatic_forward
    ):
        message.delete()
        sender_chat = message.sender_chat
        bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)


ANTICHANNEL_HANDLER = CommandHandler(["antichannel"], antichannel, run_async=True)

dispatcher.add_handler(ANTICHANNEL_HANDLER)
