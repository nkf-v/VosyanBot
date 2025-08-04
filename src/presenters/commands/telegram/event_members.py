from telegram import Update
from telegram.ext import ContextTypes

from src.applications.event_members.invite import EventMemberInvite, EventMemberInviteParams
from src.applications.event_members.leave import EventMemberLeave, EventMemberLeaveParams
from src.repositories import EventRepository, EventMemberRepository

from src.infrastructure.logger_init import logger

async def member_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    event_id = context.args[0] if context.args[0] else 0
    if not event_id.isdigit() or event_id == 0:
        context.bot.send_message(chat_id=chat_id, text='Событие не найдено')
        return

    user_info = await context.bot.get_chat_member(chat_id, member_id)
    user_name = user_info.user.full_name
    nick_name = user_info.user.username

    invite = EventMemberInvite(
        event_repository=EventRepository(),
        event_member_repository=EventMemberRepository()
    )

    params = EventMemberInviteParams(
        event_id=event_id,
        chat_id=chat_id,
        member_id=member_id,
        user_name=user_name,
        nick_name=nick_name,
    )
    message = invite.execute(params)

    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except:
        logger.error(f"Failed send message {message}")



async def member_leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    event_id = context.args[0] if context.args[0] else 0
    if not event_id.isdigit() or event_id == 0:
        context.bot.send_message(chat_id=chat_id, text='Событие не найдено')
        return

    leave = EventMemberLeave(
        event_repository=EventRepository(),
        event_member_repository=EventMemberRepository()
    )

    params = EventMemberLeaveParams(
        event_id=event_id,
        chat_id=chat_id,
        member_id=member_id,
    )
    message = leave.execute(params)

    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except:
        logger.error(f"Failed send message {message}")