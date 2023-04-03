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
from time import time
from html import escape
from traceback import format_exc
from Suzune.utils.cache import (ADMIN_CACHE, TEMP_ADMIN_CACHE_BLOCK,
                                  admin_cache_reload)
from pyrogram.errors import (ChatAdminInviteRequired, ChatAdminRequired,
                             FloodWait, RightForbidden, RPCError,
                             UserAdminInvalid)
from pyrogram.enums import ChatType
from pyrogram import enums, filters
from pyrogram.types import CallbackQuery, ChatPermissions, Message, ChatPrivileges
from Suzune.utils.adminchk import admin_check, extract_user
from Suzune.utils.sax import mention_markdown, mention_html
from Suzune import BOT_ID, SUDOERS, app, LOGGER
from Suzune.sys.decorators.errors import capture_err
from Suzune.sys.keyboard import ikb
from Suzune.utils.dbfunctions import (
    add_warn,
    get_warn,
    int_to_alpha,
    remove_warns,
    save_filter,
)
from Suzune.utils.functions import (
    extract_user,
    extract_user_and_reason,
    time_converter,
)

source_dict = "Admin"
help_dict = """/ban - Ban A User
/dban - Delete the replied message banning its sender
/tban - Ban A User For Specific Time
/unban - Unban A User
/warn - Warn A User
/dwarn - Delete the replied message warning its sender
/rmwarns - Remove All Warning of A User
/warns - Show Warning Of A User
/kick - Kick A User
/dkick - Delete the replied message kicking its sender
/purge - Purge Messages
/del - Delete Replied Message
/promote - Promote A Member
/fullpromote - Promote A Member With All Rights
/demote - Demote A Member
/pin - Pin A Message
/mute - Mute A User
/tmute - Mute A User For Specific Time
/unmute - Unmute A User
/report | @admins | @admin - Report A Message To Admins."""


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id).privileges
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


from Suzune.sys.decorators.permissions import adminsOnly


async def list_admins(chat_id: int):
    admins_in_chat = {}
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in app.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def current_chat_permissions(chat_id):
    perms = []
    perm = (await app.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms


# Get List Of Members In A Chat


async def list_members(group_id):
    return [member.user.id async for member in app.get_chat_members(group_id)]


# Purge Messages


@app.on_message(filters.command("purge") & ~filters.private)
@adminsOnly("can_delete_messages")
async def purgeFunc(_, message: Message):
    await message.delete()

    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to purge from.")

    chat_id = message.chat.id
    message_ids = []

    for message_id in range(
        message.reply_to_message.id,
        message.id,
    ):
        message_ids.append(message_id)

        # Max message deletion limit is 100
        if len(message_ids) == 100:
            await app.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,  # For both sides
            )

            # To delete more than 100 messages, start again
            message_ids = []

    # Delete if any messages left
    if message_ids:
        await app.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )


# Kick members


@app.on_message(filters.command(["kick", "dkick"]) & ~filters.private)
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text(
            "I can't kick myself, i can leave if you want."
        )
    if user_id in SUDOERS:
        return await message.reply_text("You Wanna Kick The Elevated One?")
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "I can't kick an admin, You know the rules, so do i."
        )
    mention = (await app.get_users(user_id)).mention
    msg = f"""
**Kicked User:** {mention}
**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}
**Reason:** {reason or 'No Reason Provided.'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)


# Ban members


@app.on_message(filters.command(["ban", "dban", "tban"]) & ~filters.private)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text(
            "I can't ban myself, i can leave if you want."
        )
    if user_id in SUDOERS:
        return await message.reply_text(
            "You Wanna Ban The Elevated One?, RECONSIDER!"
        )
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "I can't ban an admin, You know the rules, so do i."
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"**Banned User:** {mention}\n"
        f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"**Banned For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                await message.reply_text(msg)
            else:
                await message.reply_text("You can't use more than 99")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)


# Unban members


@app.on_message(filters.command("unban") & ~filters.private)
@adminsOnly("can_restrict_members")
async def unbanFunc(_, message: Message):
    # we don't need reasons for unban, also, we
    # don't need to get "text_mention" entity, because
    # normal users won't get text_mention if the the user
    # they want to unban is not in the group.
    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and message.reply_to_message:
        user = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "Provide a username or reply to a user's message to unban."
        )
    await message.chat.unban_member(user)
    umention = (await app.get_users(user)).mention
    await message.reply_text(f"Unbanned! {umention}")


# Delete messages


@app.on_message(filters.command("del") & ~filters.private)
@adminsOnly("can_delete_messages")
async def deleteFunc(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message To Delete It")
    await message.reply_to_message.delete()
    await message.delete()


@app.on_message(filters.command("promote") & ~filters.private)
async def promote_usr(c: app, m: Message):
    global ADMIN_CACHE
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(
            text="Please provide a user_id/username or reply to a message"
        )
        return
    try:
        user_id, user_first_name, user_name = await extract_user(c, m)
    except Exception:
        return
    bot = await c.get_chat_member(m.chat.id, BOT_ID)
    if user_id == BOT_ID:
        await m.reply_text("I can't promote myself.")
        return
    if not bot.privileges.can_promote_members:
        return await m.reply_text(
            "I don't have enough permissions",
        )  # This should be here
    # If user is alreay admin
    try:
        admin_list = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admin_list = {
            i[0] for i in (await admin_cache_reload(m, "promote_cache_update"))
        }
    if user_id in admin_list:
        await m.reply_text(
            "This user is already an admin, how am I supposed to re-promote them?",
        )
        return
    try:
        await m.chat.promote_member(
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=bot.privileges.can_change_info,
                can_invite_users=bot.privileges.can_invite_users,
                can_delete_messages=bot.privileges.can_delete_messages,
                can_restrict_members=bot.privileges.can_restrict_members,
                can_pin_messages=bot.privileges.can_pin_messages,
                can_manage_chat=bot.privileges.can_manage_chat,
                can_manage_video_chats=bot.privileges.can_manage_video_chats,
            ),
        )
        title = ""
        if m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            title = "-Admin-"  # Deafult title
            if len(m.text.split()) == 3 and not m.reply_to_message:
                title = m.text.split()[2]
            elif len(m.text.split()) == 2 and m.reply_to_message:
                title = m.text.split()[1]
            if title and len(title) > 16:
                title = title[0:16]  # trim title to 16 characters

            try:
                await c.set_administrator_title(m.chat.id, user_id, title)
            except RPCError as e:
                LOGGER.error(e)
        LOGGER.info(
            f"{m.from_user.id} promoted {user_id} in {m.chat.id} with title '{title}'",
        )
        await m.reply_text(
            ("{promoter} promoted {promoted} in chat <b>{chat_title}</b>!").format(
                promoter=(await mention_html(m.from_user.first_name, m.from_user.id)),
                promoted=(await mention_html(user_first_name, user_id)),
                chat_title=f"{escape(m.chat.title)} title set to {title}"
                if title
                else f"{escape(m.chat.title)} title set to default",
            ),
        )
        try:
            inp1 = user_name or user_first_name
            admins_group = ADMIN_CACHE[m.chat.id]
            admins_group.append((user_id, inp1))
            ADMIN_CACHE[m.chat.id] = admins_group
        except KeyError:
            await admin_cache_reload(m, "promote_key_error")
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to promote this user.")
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RPCError as e:
        await m.reply_text(
            text=f"Some error occured, report to @Suzune_Support \n <b>Error:</b> <code>{e}</code>"
        )
        LOGGER.error(e)
        LOGGER.error(format_exc())
    return
        

# Demote Member


@app.on_message(filters.command("demote") & ~filters.private)
async def demote_usr(c: app, m: Message):
    await m.reply_text("`Trying to Demote user...`")
    is_admin = await admin_check(c, m)
    if not is_admin:
        return
        return
    user_id, user_first_name = await extract_user(m)
    try:
        await m.chat.promote_member(
            user_id=user_id,
            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
        )
        await asyncio.sleep(2)
        if str(user_id).lower().startswith("@"):
            await m.reply_text(f"**Demoted** {user_first_name}")
            await c.send_message(
                6185365707,
                f"#DEMOTE\nDemoted {user_first_name} in chat {m.chat.title}",
            )
        else:
            await m.reply_text(
                f"**Demoted** {mention_markdown(user_first_name, user_id)}"
            )
            await c.send_message(
                6185365707,
                "#DEMOTE\nDemoted {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), m.chat.title
                ),
            )
    except Exception as ef:
        await m.reply_text(f"**Error:**\n\n`{ef}`")

@app.on_message(filters.command(["pin", "unpin"]) & ~filters.private)
@adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to pin/unpin it.")
    r = message.reply_to_message
    if message.command[0] == "unpin":
        await r.unpin()
        return await message.reply_text(f"Unpinned {r.link}!")
    if len(message.command) > 1 and message.command[1] == "loud":
        disable_notification = False
    else:
        disable_notification = True
    await r.pin(disable_notification=disable_notification)
    await message.reply(
        f"**Pinned [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )
    msg = f"Please check the pinned message: {r.link}"
    filter_ = dict(type="text", data=msg)
    await save_filter(message.chat.id, "~pinned", filter_)


# Mute members


@app.on_message(filters.command(["mute", "tmute"]) & ~filters.private)
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text("I can't mute myself.")
    if user_id in SUDOERS:
        return await message.reply_text(
            "You wanna mute the elevated one?, RECONSIDER!"
        )
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "I can't mute an admin, You know the rules, so do i."
        )
    mention = (await app.get_users(user_id)).mention
    keyboard = ikb({"🚨   Unmute   🚨": f"unmute_{user_id}"})
    msg = (
        f"**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0] == "tmute":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_mute = await time_converter(message, time_value)
        msg += f"**Muted For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.restrict_member(
                    user_id,
                    permissions=ChatPermissions(),
                    until_date=temp_mute,
                )
                await message.reply_text(msg, reply_markup=keyboard)
            else:
                await message.reply_text("You can't use more than 99")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await message.reply_text(msg, reply_markup=keyboard)


# Unmute members


@app.on_message(filters.command("unmute") & ~filters.private)
@adminsOnly("can_restrict_members")
async def unmute(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    await message.reply_text(f"Unmuted! {umention}")



@app.on_message(filters.command(["warn", "dwarn"]) & ~filters.private)
@adminsOnly("can_restrict_members")
async def warn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text(
            "I can't warn myself, i can leave if you want."
        )
    if user_id in SUDOERS:
        return await message.reply_text(
            "You Wanna Warn The Elevated One?, RECONSIDER!"
        )
    if user_id in (await list_admins(chat_id)):
        return await message.reply_text(
            "I can't warn an admin, You know the rules, so do i."
        )
    if user_id not in (await list_members(chat_id)):
        return await message.reply_text("This user isn't here.")
    user, warns = await asyncio.gather(
        app.get_users(user_id),
        get_warn(chat_id, await int_to_alpha(user_id)),
    )
    mention = user.mention
    keyboard = ikb({"🚨  Remove Warn  🚨": f"unwarn_{user_id}"})
    warns = warns["warns"] if warns else 0
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(
            f"Number of warns of {mention} exceeded, BANNED!"
        )
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        msg = f"""
**Warned User:** {mention}
**Warned By:** {message.from_user.mention if message.from_user else 'Anon'}
**Reason:** {reason or 'No Reason Provided.'}
**Warns:** {warns + 1}/3"""
        await message.reply_text(msg, reply_markup=keyboard)
        await add_warn(chat_id, await int_to_alpha(user_id), warn)


@app.on_callback_query(filters.regex("unwarn_"))
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await cq.answer(
            "You don't have enough permissions to perform this action.\n"
            + f"Permission needed: {permission}",
            show_alert=True,
        )
    user_id = cq.data.split("_")[1]
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if not warns or warns == 0:
        return await cq.answer("User has no warnings.")
    warn = {"warns": warns - 1}
    await add_warn(chat_id, await int_to_alpha(user_id), warn)
    text = cq.message.text.markdown
    text = f"~~{text}~~\n\n"
    text += f"__Warn removed by {from_user.mention}__"
    await cq.message.edit(text)


# Rmwarns


@app.on_message(filters.command("rmwarns") & ~filters.private)
@adminsOnly("can_restrict_members")
async def remove_warnings(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to remove a user's warnings."
        )
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if warns == 0 or not warns:
        await message.reply_text(f"{mention} have no warnings.")
    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply_text(f"Removed warnings of {mention}.")


# Warns


@app.on_message(filters.command("warns") & ~filters.private)
@capture_err
async def check_warns(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    warns = await get_warn(message.chat.id, await int_to_alpha(user_id))
    mention = (await app.get_users(user_id)).mention
    if warns:
        warns = warns["warns"]
    else:
        return await message.reply_text(f"{mention} has no warnings.")
    return await message.reply_text(f"{mention} has {warns}/3 warnings.")


# Report


@app.on_message(
    (
        filters.command("report")
        | filters.command(["admins", "admin"], prefixes="@")
    )
    & ~filters.private
)
@capture_err
async def report_user(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to report that user."
        )

    if message.reply_to_message.from_user.id == message.from_user.id:
        return await message.reply_text("Why are you reporting yourself ?")

    list_of_admins = await list_admins(message.chat.id)
    if message.reply_to_message.from_user.id in list_of_admins:
        return await message.reply_text(
            "Do you know that the user you are replying is an admin ?"
        )

    user_mention = message.reply_to_message.from_user.mention
    text = f"Reported {user_mention} to admins!"
    admin_data = await app.get_chat_members(
        chat_id=message.chat.id, filter="administrators"
    )  # will it giv floods ?
    for admin in admin_data:
        if admin.user.is_bot or admin.user.is_deleted:
            # return bots or deleted admins
            continue
        text += f"[\u2063](tg://user?id={admin.user.id})"

    await message.reply_to_message.reply_text(text)
