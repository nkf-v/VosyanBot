from telegram import Update
from telegram.ext import ContextTypes

from src.applications.events import create
from src.applications.events.delete import EventDelete, EventDeleteParams
from src.applications.events.get_list import GetEventList
from src.applications.events.remind import EventRemind, EventRemindParams
from src.applications.events.update import EventUpdate, EventUpdateParams
from src.infrastructure.logger_init import logger
from src.models import db
from src.repositories import EventRepository, EventMemberRepository

async def event_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    text = ' '.join(context.args) if context.args[0] else ''

    if text == '':
        context.bot.send_message(chat_id=chat_id, text='Придумай название своему бесполезному событию')
        return

    username = update.message.from_user.username
    full_name = update.message.from_user.full_name


    event_create_executor = create.CreateEvent(
        event_repository=EventRepository(db),
        event_member_repository=EventMemberRepository(db)
    )

    params = create.CreateEvenParams(
        chat_id,
        member_id,
        text,
        username,
        full_name,
    )

    message = event_create_executor.execute(params)

    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except:
        logger.error(f"Failed send message {message}")

async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    getter = GetEventList(
        repository=EventRepository(db),
        event_member_repository=EventMemberRepository(db)
    )

    messages = getter.execute(
        chat_id=chat_id,
        member_id=member_id,
    )

    message = '\n'.join(messages)

    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except:
        logger.error(f"Failed send message {message}")


async def event_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    args = context.args

    event_id = args[0] if args[0] else 0
    if not event_id.isdigit() or event_id == 0:
        context.bot.send_message(chat_id=chat_id, text='Событие не найдено')
        return

    args.pop(0)

    text = ' '.join(args) if args[0] else ''

    if text == '':
        context.bot.send_message(chat_id=chat_id, text='Придумай название своему бесполезному событию')
        return

    updater = EventUpdate(
        repository=EventRepository(db)
    )

    params = EventUpdateParams(
        chat_id,
        member_id,
        event_id,
        text,
    )

    message = updater.execute(params)

    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except:
        logger.error(f"Failed send message {message}")


async def event_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    event_id = context.args[0] if context.args[0] else 0
    if not event_id.isdigit() or event_id == 0:
        context.bot.send_message(chat_id=chat_id, text='Событие не найдено')
        return

    deleter = EventDelete(
        repository=EventRepository(db),
        event_member_repository=EventMemberRepository(db)
    )

    params = EventDeleteParams(
        event_id,
        chat_id,
        member_id,
    )

    message = deleter.execute(params)

    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except:
        logger.error(f"Failed send message {message}")


async def event_remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    event_id = context.args[0] if context.args[0] else 0
    if not event_id.isdigit() or event_id == 0:
        context.bot.send_message(chat_id=chat_id, text='Событие не найдено')
        return

    remind = EventRemind(
        event_repository=EventRepository(db),
        event_member_repository=EventMemberRepository(db)
    )

    params = EventRemindParams(
        event_id,
        chat_id,
        member_id,
    )

    message = remind.execute(params)

    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except:
        logger.error(f"Failed send message {message}")