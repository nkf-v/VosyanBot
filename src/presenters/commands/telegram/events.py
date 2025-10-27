import re

from telegram import Update, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from src.applications.events import create
from src.applications.events.create import CreateEvent
from src.applications.events.delete import EventDelete, EventDeleteParams
from src.applications.events.get_list import GetEventList
from src.applications.events.remind import EventRemind, EventRemindParams
from src.applications.events.update import EventUpdate, EventUpdateParams
from src.infrastructure.containers.events import App
from src.infrastructure.telegram import User
from src.presenters.commands.telegram.presenters import EventListMessagePresenter, EventDetailTelegramMessagePresenter

(
    EVENT_ENTER_TEXT,
    EVENT_ENTER_IMAGE
) = range(2)

async def event_create(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
):
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

    app = App()

    app.wire(modules=[
        __name__,
        'src',
    ])

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
    event_create_executor: CreateEvent = app.event_applications().create_event()
    event_create_executor.execute(params, presenter)

    message, keyboard = presenter.present()

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard is not None else None

    await update.message.reply_text(text=message, reply_markup=reply_markup)


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id


    app = App()

    app.wire(modules=[
        __name__,
        'src',
    ])

    presenter = EventListMessagePresenter()

    getter: GetEventList = app.event_applications().get_event_list()
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
        context.bot.send_message(chat_id=chat_id, text=f'Событие {event_id} не найдено')
        return

    message_text = re.sub(r'/[\w\-_]* \d* ', '', update.message.text)

    lines = message_text.splitlines()
    name = lines[0] if lines else ''
    text = '\n'.join(lines[1:]) if len(lines) > 1 else ""

    if name == '':
        context.bot.send_message(chat_id=chat_id, text='Придумай название своему бесполезному событию')
        return

    app = App()

    app.wire(modules=[
        __name__,
        'src',
    ])

    params = EventUpdateParams(
        chat_id,
        member_id,
        event_id,
        name,
        text,
    )

    presenter = EventDetailTelegramMessagePresenter()

    updater: EventUpdate = app.event_applications().update_event()
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

    app = App()

    app.wire(modules=[
        __name__,
        'src',
    ])

    params = EventRemindParams(
        event_id,
        chat_id,
        member_id,
    )

    presenter = EventDetailTelegramMessagePresenter()

    remind: EventRemind = app.event_applications().remind_event()
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

    app = App()

    app.wire(modules=[
        __name__,
        'src',
    ])

    params = EventDeleteParams(
        event_id,
        chat_id,
        member_id,
    )

    deleter: EventDelete = app.event_applications().delete_event()
    message = deleter.execute(params)

    await context.bot.send_message(chat_id=chat_id, text=message)
