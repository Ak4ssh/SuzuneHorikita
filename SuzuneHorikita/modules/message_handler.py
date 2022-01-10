import asyncio

from loguru import logger
from pyrogram import Client, errors
from pyrogram.raw import types, functions, base

from plugins.functions import database


def pre_sender_channel_check(update: base.Update) -> bool:
    # Input checking
    try:
        # Type check: Is the incoming message a message (Not empty or service)
        if not isinstance(update, types.UpdateNewChannelMessage):
            return False

        message = update.message

        # Type check: Is the sender a channel message
        if not isinstance(message.from_id, types.PeerChannel):
            return False

        # Check is the message incoming
        if message.out:
            return False

        # Check is the message from nicked admin
        if message.peer_id == message.from_id:
            return False

        # Is the message from linked channel - First layer
        if message.fwd_from and message.fwd_from.saved_from_peer == message.fwd_from.from_id == message.from_id:
            return False

        # Pass it to handler for more filtering
        return True
    except:  # noqa
        logger.exception("An exception occurred while pre checking sender channel.")
        return False


@Client.on_raw_update()
async def message_handler(client: Client, update: base.Update, _, chats: dict):
    if not pre_sender_channel_check(update):
        return

    while True:
        try:
            # Basic data
            message = update.message
            chat_peer = types.InputChannel(
                channel_id=message.peer_id.channel_id,
                access_hash=chats[message.peer_id.channel_id].access_hash
            )
            channel_peer = types.InputPeerChannel(
                channel_id=message.from_id.channel_id,
                access_hash=chats[message.from_id.channel_id].access_hash
            )
            chat_id = int(f"-100{message.peer_id.channel_id}")
            channel_id = int(f"-100{message.from_id.channel_id}")

            # Is the message from linked channel - Final layer
            linked_chat_id = await database.get_linked_group(
                channel_peer=chat_peer
            )
            if linked_chat_id == message.from_id.channel_id:
                return

            # Check for is the channel in whitelist for this group
            if database.match_whitelist(
                    group_peer=chat_peer,
                    channel_peer=channel_peer
            ):
                return

            # Delete the message sent by channel and ban it.
            try:
                await client.send(
                    functions.channels.EditBanned(
                        channel=chat_peer,
                        participant=channel_peer,
                        banned_rights=types.ChatBannedRights(
                            until_date=0,
                            view_messages=True,
                            send_messages=True,
                            send_media=True,
                            send_stickers=True,
                            send_gifs=True,
                            send_games=True,
                            send_polls=True,
                        )
                    )
                )
                # Add record to database
                await database.add_channel_ban_list(
                    group_peer=chat_peer,
                    channel_peer=channel_peer
                )
                logger.debug(f"Banned channel {channel_id} from group {chat_id}")
            except errors.ChatAdminRequired:
                pass

            try:
                await client.delete_messages(chat_id, message.id)
            except (errors.ChatAdminRequired, errors.MessageDeleteForbidden):
                pass

            break
        except errors.FloodWait as e:
            logger.debug(f"{e}, retry after {e.x + 1} seconds...")
            await asyncio.sleep(e.x + 1)
        except errors.ChatInvalid:
            break
        except:  # noqa
            logger.exception("An exception occurred in message_handler")
            break
