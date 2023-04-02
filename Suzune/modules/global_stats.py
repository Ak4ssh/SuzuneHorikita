"""
MIT License

Copyright (c) 2021 TheVenomXD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait

from Suzune import BOT_ID, BOT_NAME, SUDOERS, app
from Suzune.sys.decorators.errors import capture_err
from Suzune.modules import ALL_MODULES
from Suzune.utils.dbfunctions import (
    get_blacklist_filters_count,
    get_filters_count,
    get_gbans_count,
    get_karmas_count,
    get_notes_count,
    get_rss_feeds_count,
    get_served_chats,
    get_served_users,
    get_warns_count,
    remove_served_chat,
)
from Suzune.utils.http import get
from Suzune.utils.inlinefuncs import keywords_list


@app.on_message(filters.command("gstats") & filters.user(SUDOERS))
@capture_err
async def global_stats(_, message):
    m = await app.send_message(
        message.chat.id,
        text="__**Analysing Stats...**__",
        disable_web_page_preview=True,
    )

    # For bot served chat and users count
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    # Gbans count
    gbans = await get_gbans_count()
    _notes = await get_notes_count()
    notes_count = _notes["notes_count"]
    notes_chats_count = _notes["chats_count"]

    # Filters count across chats
    _filters = await get_filters_count()
    filters_count = _filters["filters_count"]
    filters_chats_count = _filters["chats_count"]

    # Blacklisted filters count across chats
    _filters = await get_blacklist_filters_count()
    blacklist_filters_count = _filters["filters_count"]
    blacklist_filters_chats_count = _filters["chats_count"]

    # Warns count across chats
    _warns = await get_warns_count()
    warns_count = _warns["warns_count"]
    warns_chats_count = _warns["chats_count"]

    # Karmas count across chats
    _karmas = await get_karmas_count()
    karmas_count = _karmas["karmas_count"]
    karmas_chats_count = _karmas["chats_count"]

    # Contributors/Developers count and commits on github
    url = "https://api.github.com/repos/DesiNobita/Suzunebot/contributors"
    rurl = "https://github.com/DesiNobita/Suzunebot"
    developers = await get(url)
    commits = sum(developer["contributions"] for developer in developers)
    developers = len(developers)

    # Rss feeds
    rss_count = await get_rss_feeds_count()
    # Modules info
    modules_count = len(ALL_MODULES)

    # Userbot info
    groups_ub = channels_ub = bots_ub = privates_ub = total_ub = 0

    msg = f"""
**Global Stats of {BOT_NAME}**:
    **{modules_count}** Modules Loaded.
    **{len(keywords_list)}** Inline Modules Loaded.
    **{rss_count}** Active RSS Feeds.
    **{gbans}** Globally banned users.
    **{filters_count}** Filters, Across **{filters_chats_count}** chats.
    **{blacklist_filters_count}** Blacklist Filters, Across **{blacklist_filters_chats_count}** chats.
    **{notes_count}** Notes, Across **{notes_chats_count}** chats.
    **{warns_count}** Warns, Across **{warns_chats_count}** chats.
    **{karmas_count}** Karma, Across **{karmas_chats_count}** chats.
    **{served_users}** Users, Across **{served_chats}** chats.
    **{developers}** Developers And **{commits}** Commits On **[Github]({rurl})**.

"""
    await m.edit(msg, disable_web_page_preview=True)
