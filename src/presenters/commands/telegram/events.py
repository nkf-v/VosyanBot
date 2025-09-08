import re

from telegram import Update, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from src.applications.events import create
from src.applications.events.delete import EventDelete, EventDeleteParams
from src.applications.events.get_list import GetEventList
from src.applications.events.remind import EventRemind, EventRemindParams
from src.applications.events.update import EventUpdate, EventUpdateParams
from src.infrastructure.telegram import User
from src.models import db
from src.presenters.commands.telegram.presenters import EventListMessagePresenter, EventDetailTelegramMessagePresenter
from src.repositories import EventRepository, EventMemberRepository

(
    EVENT_ENTER_TEXT,
    EVENT_ENTER_IMAGE
) = range(2)

async def event_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    message_text = re.sub(r'/[\w\-_]* ', '', update.message.text)

    lines = message_text.splitlines()
    name = lines[0] if lines else ''
    text = '\n'.join(lines[1:]) if len(lines) > 1 else ""

    if name == '':
        context.bot.send_message(chat_id=chat_id, text='Придумай название своему бесполезному событию')
        return

    nick_name = update.message.from_user.username
    user_name = update.message.from_user.full_name


    event_create_executor = create.CreateEvent(
        event_repository=EventRepository(db),
        event_member_repository=EventMemberRepository(db)
    )

    params = create.CreateEvenParams(
        chat_id,
        member_id,
        name,
        text,
        User(
            nick_name,
            user_name,
        )
    )

    presenter = EventDetailTelegramMessagePresenter()
    event_create_executor.execute(params, presenter)

    message, keyboard = presenter.present()

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard is not None else None

    await update.message.reply_text(text=message, reply_markup=reply_markup)


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    getter = GetEventList(
        repository=EventRepository(db),
        event_member_repository=EventMemberRepository(db)
    )

    presenter = EventListMessagePresenter()

    getter.execute(
        chat_id=chat_id,
        member_id=member_id,
        presenter=presenter,
    )

    message = presenter.present()

    reply_markup = None

    if update.message.chat.type == ChatType.PRIVATE:
        keyboard = [
            ['Создать событие'],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


async def event_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    event_id = context.args[0] if context.args[0] else 0
    if not event_id.isdigit() or event_id == 0:
        context.bot.send_message(chat_id=chat_id, text='Событие не найдено')
        return

    message_text = re.sub(r'/[\w\-_]* \d* ]', '', update.message.text)

    lines = message_text.splitlines()
    name = lines[0] if lines else ''
    text = '\n'.join(lines[1:]) if len(lines) > 1 else ""

    if name == '':
        context.bot.send_message(chat_id=chat_id, text='Придумай название своему бесполезному событию')
        return

    updater = EventUpdate(
        repository=EventRepository(db),
        event_member_repository=EventMemberRepository(db),
    )

    params = EventUpdateParams(
        chat_id,
        member_id,
        event_id,
        name,
        text,
    )

    presenter = EventDetailTelegramMessagePresenter()

    updater.execute(params, presenter)

    message, keyboard = presenter.present()

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard is not None else None

    await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


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

    presenter = EventDetailTelegramMessagePresenter()
    remind.execute(params, presenter)
    message, keyboard = presenter.present()

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard is not None else None

    await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


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
