import time
from typing import List

import requests
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async

from SuzuneHorikita import StartTime, dispatcher
from SuzuneHorikita.modules.helper_funcs.chat_status import sudo_plus
from SuzuneHorikita.modules.disable import DisableAbleCommandHandler


@sudo_plus
def ping(update: Update, context: CallbackContext):
    msg = update.effective_message

    start_time = time.time()
    message = msg.reply_text("Pinging...")
    end_time = time.time()
    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    uptime = get_readable_time((time.time() - StartTime))

    message.edit_text(
        "<b>Pong!!</b>\n"
        "<b>Time Taken:</b> <code>{}</code>\n"
        "<b>Service Uptime:</b> <code>{}</code>".format(telegram_ping, uptime),
        parse_mode=ParseMode.HTML,
    )




PING_HANDLER = DisableAbleCommandHandler("ping", ping, run_async=True)

dispatcher.add_handler(PING_HANDLER)

__command_list__ = ["ping"]
__handlers__ = [PING_HANDLER]
