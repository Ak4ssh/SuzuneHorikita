import importlib
import collections

from src import dispatcher, telethn
from src.__main__ import (
    CHAT_SETTINGS,
    DATA_EXPORT,
    DATA_IMPORT,
    HELPABLE,
    IMPORTED,
    MIGRATEABLE,
    STATS,
    USER_INFO,
    USER_SETTINGS,
)
from src.source.helper_funcs.chat_status import dev_plus, sudo_plus
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler


@dev_plus
def load(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(" ", 1)[1]
    load_messasge = message.reply_text(
        f"Attempting to load module : <b>{text}</b>",
        parse_mode=ParseMode.HTML,
    )

    try:
        imported_module = importlib.import_module("src.source." + text)
    except:
        load_messasge.edit_text("Does that module even exist?")
        return

    if not hasattr(imported_module, "inline"):
        imported_module.inline = imported_module.__name__

    if imported_module.inline.lower() not in IMPORTED:
        IMPORTED[imported_module.inline.lower()] = imported_module
    else:
        load_messasge.edit_text("Module already loaded.")
        return
    if "hndrl" in dir(imported_module):
        handlers = imported_module.hndrl
        for handler in handlers:
            if not isinstance(handler, tuple):
                dispatcher.add_handler(handler)
            else:
                if isinstance(handler[0], collections.Callable):
                    callback, telethon_event = handler
                    telethn.add_event_handler(callback, telethon_event)
                else:
                    handler_name, priority = handler
                    dispatcher.add_handler(handler_name, priority)
    else:
        IMPORTED.pop(imported_module.inline.lower())
        load_messasge.edit_text("The module cannot be loaded.")
        return

    if hasattr(imported_module, "saxsux") and imported_module.saxsux:
        HELPABLE[imported_module.inline.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.inline.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.inline.lower()] = imported_module

    load_messasge.edit_text(
        "Successfully loaded module : <b>{}</b>".format(text),
        parse_mode=ParseMode.HTML,
    )


@dev_plus
def unload(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(" ", 1)[1]
    unload_messasge = message.reply_text(
        f"Attempting to unload module : <b>{text}</b>",
        parse_mode=ParseMode.HTML,
    )

    try:
        imported_module = importlib.import_module("src.source." + text)
    except:
        unload_messasge.edit_text("Does that module even exist?")
        return

    if not hasattr(imported_module, "inline"):
        imported_module.inline = imported_module.__name__
    if imported_module.inline.lower() in IMPORTED:
        IMPORTED.pop(imported_module.inline.lower())
    else:
        unload_messasge.edit_text("Can't unload something that isn't loaded.")
        return
    if "hndrl" in dir(imported_module):
        handlers = imported_module.hndrl
        for handler in handlers:
            if isinstance(handler, bool):
                unload_messasge.edit_text("This module can't be unloaded!")
                return
            if not isinstance(handler, tuple):
                dispatcher.remove_handler(handler)
            else:
                if isinstance(handler[0], collections.Callable):
                    callback, telethon_event = handler
                    telethn.remove_event_handler(callback, telethon_event)
                else:
                    handler_name, priority = handler
                    dispatcher.remove_handler(handler_name, priority)
    else:
        unload_messasge.edit_text("The module cannot be unloaded.")
        return

    if hasattr(imported_module, "saxsux") and imported_module.saxsux:
        HELPABLE.pop(imported_module.inline.lower())

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.remove(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.remove(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.remove(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.remove(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.remove(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS.pop(imported_module.inline.lower())

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS.pop(imported_module.inline.lower())

    unload_messasge.edit_text(
        f"Successfully unloaded module : <b>{text}</b>",
        parse_mode=ParseMode.HTML,
    )


@sudo_plus
def listsource(update: Update, context: CallbackContext):
    message = update.effective_message
    module_list = []

    for helpable_module in HELPABLE:
        helpable_module_info = IMPORTED[helpable_module]
        file_info = IMPORTED[helpable_module_info.inline.lower()]
        file_name = file_info.__name__.rsplit("src.source.", 1)[1]
        mod_name = file_info.inline
        module_list.append(f"- <code>{mod_name} ({file_name})</code>\n")
    module_list = "Following source are loaded : \n\n" + "".join(module_list)
    message.reply_text(module_list, parse_mode=ParseMode.HTML)


LOAD_HANDLER = CommandHandler("load", load, run_async=True)
UNLOAD_HANDLER = CommandHandler("unload", unload, run_async=True)
LISTsource_HANDLER = CommandHandler("listsource", listsource, run_async=True)

dispatcher.add_handler(LOAD_HANDLER)
dispatcher.add_handler(UNLOAD_HANDLER)
dispatcher.add_handler(LISTsource_HANDLER)

inline = "source"
