import asyncio
import time
from typing import Optional, Union

from loguru import logger
from pyrogram import errors
from pyrogram.raw import types, base, functions

from plugins.glovar import linked_channel_db, whitelist_db, stat_db

link_ch_db_lock: asyncio.Lock = asyncio.Lock()
whitelist_db_lock: asyncio.Lock = asyncio.Lock()
stat_db_lock: asyncio.Lock = asyncio.Lock()


async def get_linked_group(*, channel_peer: base.InputChannel = None, channel_id: int = None) -> Optional[int]:
    """
    Get linked group by channel peer or channel id
    :param channel_peer: Channel peer
    :param channel_id: Channel id
    :raise ValueError: Both channel_peer and channel_id is not set
    :return: Group id
    """
    from plugins.glovar import bot_client

    # Check for channel_peer and channel_id is set
    if channel_peer is None and channel_id is None:
        raise ValueError("channel_peer or channel_id must be set.")
    elif channel_peer is None:
        channel_peer = types.InputChannel(
            channel_id=channel_id,
            access_hash=0
        )

    # Basic data
    chat_id = channel_id or channel_peer.channel_id
    cur = linked_channel_db.cursor()

    try:
        # Check is the id available in database first
        cur.execute("select channel_id, update_time from CHANNEL_LINKED_GROUP where group_id = ?;", (chat_id,))
        query_result = cur.fetchone()

        if query_result is not None:
            channel_id, update_time = query_result

            # Determine cached linked_chat_id is available
            if time.time() - update_time < 300:
                return channel_id

        # Get channel info by requesting
        result: types.messages.ChatFull
        if channel_peer is not None:
            result = await bot_client.send(
                functions.channels.GetFullChannel(
                    channel=channel_peer
                )
            )
        else:
            return None

        current_timestamp = int(time.time()) - 1
        linked_chat_id = result.full_chat.linked_chat_id

        # Update data in database
        sql_query = "insert or replace into CHANNEL_LINKED_GROUP (group_id, channel_id, update_time) values (?, ?, ?);"
        async with link_ch_db_lock:
            cur.execute(sql_query, (chat_id, linked_chat_id, current_timestamp))
            linked_channel_db.commit()

        return linked_chat_id
    except errors.FloodWait as e:
        logger.debug(f"{e}, retry after {e.x + 1} seconds...")
        await asyncio.sleep(e.x + 1)
        return await get_linked_group(channel_peer=channel_peer, channel_id=channel_id)
    except errors.ChannelInvalid:
        return None
    except:  # noqa
        logger.exception(f"Error whiling getting linked group {chat_id}")
    finally:
        cur.close()

    return None


def match_whitelist(*,
                    group_peer: base.InputChannel = None, group_id: int = None,
                    channel_peer: Union[base.InputChannel, types.InputPeerChannel] = None,
                    channel_id: int = None) -> bool:
    """
    Check is the channel in the group's whitelist
    :param group_peer: Channel Peer of the group
    :param group_id: Group ID
    :param channel_peer: Channel Peer of the channel to be added
    :param channel_id: Channel ID
    :raise ValueError: (group_peer and group_id or/and channel_peer and channel_id) is not set
    :return: The match result
    """

    # Check for group_peer and group_id is set
    if channel_peer is None and channel_id is None:
        raise ValueError("channel_peer or channel_id must be set.")
    elif group_peer is None and group_id is None:
        raise ValueError("group_peer or group_id must be set.")

    # Basic data
    chat_id = group_id or group_peer.channel_id
    channel_id = channel_id or channel_peer.channel_id
    cur = whitelist_db.cursor()

    try:
        # Check is the id available in database first
        cur.execute("select id from WHITELISTED_CHANNELS where group_id = ? and channel_id = ?;", (chat_id, channel_id))
        return cur.fetchone() is not None
    except:  # noqa
        logger.exception(f"Error whiling matching whitelist for group {chat_id} with {channel_id}")
    finally:
        cur.close()

    return False


async def add_whitelist(*,
                        group_peer: base.InputChannel = None, group_id: int = None,
                        channel_peer: Union[base.InputChannel, types.InputPeerChannel] = None,
                        channel_id: int = None) -> bool:
    """
    Add a channel to group whitelist
    :param group_peer: Channel Peer of the group
    :param group_id: Group ID
    :param channel_peer: Channel Peer of the channel to be added
    :param channel_id: Channel ID
    :raise ValueError: (group_peer and group_id or/and channel_peer and channel_id) is not set
    :return: Result of adding
    """

    # Check for group_peer and group_id or channel_peer and channel_id is set
    if channel_peer is None and channel_id is None:
        raise ValueError("channel_peer or channel_id must be set.")
    elif group_peer is None and group_id is None:
        raise ValueError("group_peer or group_id must be set.")

    # Basic data
    chat_id = group_id or group_peer.channel_id
    channel_id = channel_id or channel_peer.channel_id
    cur = whitelist_db.cursor()
    stat_cur = stat_db.cursor()

    try:
        # Check is channel id and group id already whitelisted first
        cur.execute("select id from WHITELISTED_CHANNELS where group_id = ? and channel_id = ?;",
                    (chat_id, channel_id))
        query_result = cur.fetchone()

        # Determine if the channel is already whitelist
        if query_result is not None:
            return True

        # Add channel to whitelist
        sql_query = "insert into WHITELISTED_CHANNELS (group_id, channel_id) values (?, ?);"
        async with whitelist_db_lock:
            cur.execute(sql_query, (chat_id, channel_id))
            whitelist_db.commit()

        # Ignore channel stat from that group (If previously exist)
        stat_cur.execute("select id from BANNED_CHANNELS where group_id = ? and channel_id = ?;", (chat_id, channel_id))
        query_result = stat_cur.fetchone()
        if query_result is not None:
            sql_query = "update BANNED_CHANNELS set whitelisted = false where group_id = ? and channel_id = ?;"
            async with stat_db_lock:
                stat_cur.execute(sql_query, (chat_id, channel_id))
                stat_db.commit()

        return True
    except:  # noqa
        logger.exception(f"Error while adding whitelist for group {chat_id} with channel {channel_id}")
    finally:
        stat_cur.close()
        cur.close()

    return False


async def remove_whitelist(*,
                           group_peer: base.InputChannel = None, group_id: int = None,
                           channel_peer: Union[base.InputChannel, types.InputPeerChannel] = None,
                           channel_id: int = None) -> bool:
    """
    Remove a channel in group whitelist
    :param group_peer: Channel Peer of the group
    :param group_id: Group ID
    :param channel_peer: Channel Peer of the channel to be added
    :param channel_id: Channel ID
    :raise ValueError: (group_peer and group_id or/and channel_peer and channel_id) is not set
    :return: Result of removing
    """

    # Check for group_peer and group_id or channel_peer and channel_id is set
    if channel_peer is None and channel_id is None:
        raise ValueError("channel_peer or channel_id must be set.")
    elif group_peer is None and group_id is None:
        raise ValueError("group_peer or group_id must be set.")

    # Basic data
    chat_id = group_id or group_peer.channel_id
    channel_id = channel_id or channel_peer.channel_id
    cur = whitelist_db.cursor()

    try:
        # Check is channel id and group id already whitelisted first
        cur.execute("select id from WHITELISTED_CHANNELS where group_id = ? and channel_id = ?;",
                    (chat_id, channel_id))
        query_result = cur.fetchone()

        # Determine if the channel is already whitelist
        if query_result is None:
            return False

        # Remove channel from whitelist
        sql_query = "delete from WHITELISTED_CHANNELS where group_id = ? and channel_id = ?;"
        async with whitelist_db_lock:
            cur.execute(sql_query, (chat_id, channel_id))
            whitelist_db.commit()

        return True
    except:  # noqa
        logger.exception(f"Error while removing whitelist for group {chat_id} with channel {channel_id}")
    finally:
        cur.close()

    return False


async def add_channel_ban_list(*,
                               group_peer: base.InputChannel = None, group_id: int = None,
                               channel_peer: Union[base.InputChannel, types.InputPeerChannel] = None,
                               channel_id: int = None) -> bool:
    """
    Add a channel to ban list (stat)
    :param group_peer: Channel Peer of the group
    :param group_id: Group ID
    :param channel_peer: Channel Peer of the channel to be added
    :param channel_id: Channel ID
    :raise ValueError: (group_peer and group_id or/and channel_peer and channel_id) is not set
    :return: Add result
    """

    # Check for group_peer and group_id or channel_peer and channel_id is set
    if channel_peer is None and channel_id is None:
        raise ValueError("channel_peer or channel_id must be set.")
    elif group_peer is None and group_id is None:
        raise ValueError("group_peer or group_id must be set.")

    # Basic data
    chat_id = group_id or group_peer.channel_id
    channel_id = channel_id or channel_peer.channel_id
    cur = stat_db.cursor()

    try:
        # Check is channel id and group id already banned first
        cur.execute("select id from BANNED_CHANNELS where group_id = ? and channel_id = ?;",
                    (chat_id, channel_id))
        query_result = cur.fetchone()

        # Determine if the channel is already banned
        if query_result is None:
            # Add channel to ban list
            sql_query = ("insert or replace into BANNED_CHANNELS (group_id, channel_id, whitelisted) "
                         "values (?, ?, false);")
            async with stat_db_lock:
                cur.execute(sql_query, (chat_id, channel_id))
                stat_db.commit()

        return True
    except:  # noqa
        logger.exception(f"Error while adding channel {channel_id} to ban list for group {chat_id}")
    finally:
        cur.close()

    return False


def get_banned_channels_count(*, group_peer: base.InputChannel = None, group_id: int = None) -> Optional[int]:
    """
    Get total of banned channels
    :param group_peer: Channel Peer of the group
    :param group_id: Group ID
    :raise ValueError: group_peer and group_id is not set
    :return: Number of banned channel(s)
    """

    # Check for group_peer and group_id is set
    if group_peer is None and group_id is None:
        raise ValueError("group_peer or group_id must be set.")

    # Basic data
    chat_id = group_id or group_peer.channel_id
    cur = stat_db.cursor()

    try:
        # Get sum of banned channels
        cur.execute("select count(id) from BANNED_CHANNELS where group_id = ? and whitelisted = false;", (chat_id,))
        query_result = cur.fetchone()

        if query_result is not None:
            return query_result[0]
    except:  # noqa
        logger.exception(f"Error while counting total banned channels for group {chat_id}")
    finally:
        cur.close()


async def clear_channel_stat_data(*, group_peer: base.InputChannel = None, group_id: int = None) -> Optional[int]:
    """
    Clear all statistics data (Banned channel from that group) in database
    :param group_peer: Channel Peer of the group
    :param group_id: Group ID
    :raise ValueError: group_peer and group_id is not set
    :return: Cleaned channel record
    """

    # Check for group_peer and group_id is set
    if group_peer is None and group_id is None:
        raise ValueError("group_peer or group_id must be set.")

    # Basic data
    chat_id = group_id or group_peer.channel_id
    cur = stat_db.cursor()

    try:
        # Get sum of banned channels
        cur.execute("select count(id) from BANNED_CHANNELS where group_id = ?;", (chat_id,))
        query_result = cur.fetchone()

        if query_result is None or (query_result and query_result[0] == 0):
            return

        async with stat_db_lock:
            cur.execute("delete from BANNED_CHANNELS where group_id = ?;", (chat_id,))
            stat_db.commit()

        return query_result[0]
    except:  # noqa
        logger.exception(f"Error while clearing banned channel stat for group {chat_id}")
    finally:
        cur.close()
