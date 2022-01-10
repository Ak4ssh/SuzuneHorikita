import sqlite3
import sys
from configparser import RawConfigParser
from typing import Optional, Union

from loguru import logger
from pyrogram import Client

bot_client: Optional[Client] = None
bot_name: Optional[str] = None
linked_channel_db: sqlite3.Connection = sqlite3.connect("link_channel_cache.sqlite")
whitelist_db: sqlite3.Connection = sqlite3.connect("whitelist_data.sqlite")
stat_db: sqlite3.Connection = sqlite3.connect("stat_data.sqlite")

# [settings]
prefix: list = ["/"]

try:
    config = RawConfigParser()
    config.read("config.ini")

    # [settings]
    prefix = list(config.get("basic", "prefix", fallback=prefix))

except:  # noqa
    logger.exception("Failed to read data from config.ini, please check traceback.")
    sys.exit(1)

# Value verify
if (
        # [settings]
        prefix in ("", "[DATA EXPUNGED]") or
        prefix == []
):
    raise SystemExit("No proper settings")
