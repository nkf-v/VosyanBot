from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.applications.events import create
from src.applications.events.delete import EventDelete, EventDeleteParams
from src.applications.events.get_list import GetEventList, EventListPresenter
from src.applications.events.remind import EventRemind, EventRemindParams, EventRemindResult
from src.applications.events.update import EventUpdate, EventUpdateParams
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

    result = EventRemindResult()
    event_create_executor.execute(params, result)

    message, keyboard = result.present()

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard is not None else None

    await update.message.reply_text(text=message, reply_markup=reply_markup)

async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    getter = GetEventList(
        repository=EventRepository(db),
        event_member_repository=EventMemberRepository(db)
    )

    presenter = EventListPresenter()

    getter.execute(
        chat_id=chat_id,
        member_id=member_id,
        presenter=presenter,
    )

    message = presenter.present()

    await context.bot.send_message(chat_id=chat_id, text=message)


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

    await context.bot.send_message(chat_id=chat_id, text=message)


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

    await context.bot.send_message(chat_id=chat_id, text=message)


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

    result = EventRemindResult()
    remind.execute(params, result)
    message, keyboard = result.present()

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard is not None else None

    await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)
