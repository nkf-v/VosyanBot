import html
import json
import os
import sys
import time
import traceback

import telegram.error
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, \
    filters

import src.messages as messages
import src.stickers as stickers
from src.applications.members.registry import MemberRegistration, MemberRegistrationDto
from src.applications.members.unregister import MemberUnregister
from src.db_functions import (unreg_in_data, is_not_time_expired, are_carmic_dices_enabled, update_pidor_stats,
                              get_current_user, get_user_percentage_nice_pidor, get_pidor_stats, get_all_members,
                              get_random_id, get_random_id_carmic, get_full_name_from_db, get_nickname_from_db,
                              set_full_name_and_nickname_in_db, update_current,
                              get_chat_members_nice_coefficients, get_chat_members_pidor_coefficients)
from src.infrastructure.logger_init import logger
from src.models import db
from src.presenters.commands.telegram import events
from src.presenters.commands.telegram.keyboard_handler import keyboard_handle
from src.repositories import (
    MemberRepository,
    StatsRepository,
    PidorStsatsRepository,
    CurrentNiceRepository,
    CurrentPidorRepository
)


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    logger.error(
        "Uncaught exception, application will terminate.",
        exc_info=(exc_type, exc_value, exc_traceback),
    )

    # TODO отправку сообщения переделать в handler логирования
    tb_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
    tb_string = "".join(tb_list)

    message = (
        "Exception\n"
        "<b>Trace</b>\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    bot = Bot(os.getenv('BOT_TOKEN'))
    bot.send_message(
        chat_id=os.getenv('DEVELOPERT_CHAT_ID'),
        text=message,
        parse_mode=ParseMode.HTML
    )

sys.excepthook = handle_uncaught_exception

async def reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id
    user_info = await context.bot.get_chat_member(chat_id, member_id)
    user_full_name = user_info.user.full_name
    user_nickname = user_info.user.username

    registration = MemberRegistration(
        member_repository=MemberRepository(db),
        stats_repository=StatsRepository(db),
        pidor_stats_repository=PidorStsatsRepository(db),
        current_nice_repository=CurrentNiceRepository(db),
        current_pidor_repository=CurrentPidorRepository(db)
    )

    message = registration.execute(
        params=MemberRegistrationDto(
            chat_id=chat_id,
            member_id=member_id,
            user_full_name=user_full_name,
            user_nickname=user_nickname
        )
    )

    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except:
        logger.error(f"Failed send message {message}")


async def unreg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    member_id = update.message.from_user.id

    logger.info(f"Unreg {member_id}")

    member_repository = MemberRepository(db)
    unregister = MemberUnregister(
        repository=member_repository
    )

    message = unregister.execute(
        chat_id=chat_id,
        member_id=member_id
    )

    logger.info(f"Unreg message '{message}'")

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=message
        )
    except:
        logger.error(f"Failed send message '{message}'")


async def pidor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    congratulations = ""
    if is_not_time_expired(chat_id, 'current_pidor'):
        current_pidor_id = get_current_user(chat_id, 'current_pidor')['id']
        try:
            user_info = await context.bot.get_chat_member(chat_id, current_pidor_id)
            user_full_name = user_info.user.full_name
            user_nickname = user_info.user.username
            set_full_name_and_nickname_in_db(chat_id, current_pidor_id, user_full_name, user_nickname)
            message = f'Пидор дня уже определён, это {user_full_name} (@{user_nickname})'
        except telegram.error.BadRequest:
            user_full_name_from_db = get_full_name_from_db(chat_id, current_pidor_id)
            message = f'Пидор дня уже определён, это {user_full_name_from_db}'
    else:
        if are_carmic_dices_enabled(chat_id):
            pidor_id = get_random_id_carmic(chat_id, 'pidor')
        else:
            pidor_id = get_random_id(chat_id, 'pidor')
        if pidor_id == 'Nothing':
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Невозможно выбрать пидора, список '
                                                                                  'кандидатов пуст')
            return
        pidor_count = update_pidor_stats(chat_id, pidor_id, 'pidor_stats')
        try:
            user_info = await context.bot.get_chat_member(chat_id, pidor_id)
            user_full_name = user_info.user.full_name
            user_nickname = user_info.user.username
            set_full_name_and_nickname_in_db(chat_id, pidor_id, user_full_name, user_nickname)
            message = f'Пидор дня - {user_full_name}  (@{user_nickname})'
        except telegram.error.BadRequest:
            user_full_name_from_db = get_full_name_from_db(chat_id, pidor_id)
            user_nickname_from_db = get_nickname_from_db(chat_id, pidor_id)
            message = f'Пидор дня - {user_full_name_from_db} (@{user_nickname_from_db})'
        update_current(chat_id, 'current_pidor', pidor_id)
        for i in messages.PIDOR_MESSAGES:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=i)
            time.sleep(1)
        if pidor_count == 1:
            congratulations = messages.PIDOR_1_TIME
        if pidor_count == 10:
            congratulations = messages.TEN_TIMES
        if pidor_count == 50:
            congratulations = messages.FIFTEEN_TIMES
        if pidor_count == 100:
            congratulations = messages.HUNDRED_TIMES
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    if congratulations != "":
        await context.bot.send_message(chat_id=update.effective_chat.id, text=congratulations)
        await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                       sticker=stickers.BILLY_TEAR_OFF_VEST)


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    congratulations = ""
    if is_not_time_expired(chat_id, 'current_nice'):
        current_nice_id = get_current_user(chat_id, 'current_nice')['id']
        try:
            user_info = await context.bot.get_chat_member(chat_id, current_nice_id)
            user_full_name = user_info.user.full_name
            user_nickname = user_info.user.username
            set_full_name_and_nickname_in_db(chat_id, current_nice_id, user_full_name, user_nickname)
            message = f'Красавчик дня уже определён, это {user_full_name} (@{user_nickname})'
        except telegram.error.BadRequest:
            user_full_name_from_db = get_full_name_from_db(chat_id, current_nice_id)
            message = f'Красавчик дня уже определён, это {user_full_name_from_db}'
    else:
        if are_carmic_dices_enabled(chat_id):
            nice_guy_id = get_random_id_carmic(chat_id, 'nice')
        else:
            nice_guy_id = get_random_id(chat_id, 'nice')
        if nice_guy_id == 'Nothing':
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Невозможно выбрать красавчика, '
                                                                                  'список кандидатов пуст')
            return
        pidor_count = update_pidor_stats(chat_id, nice_guy_id, 'stats')
        try:
            user_info = await context.bot.get_chat_member(chat_id, nice_guy_id)
            user_full_name = user_info.user.full_name
            user_nickname = user_info.user.username
            set_full_name_and_nickname_in_db(chat_id, nice_guy_id, user_full_name, user_nickname)
            message = f'Красавчик дня - {user_full_name}  (@{user_nickname})'
        except telegram.error.BadRequest:
            user_full_name_from_db = get_full_name_from_db(chat_id, nice_guy_id)
            user_nickname_from_db = get_nickname_from_db(chat_id, nice_guy_id)
            message = f'Красавчик дня - {user_full_name_from_db} (@{user_nickname_from_db})'
        update_current(chat_id, 'current_nice', nice_guy_id)
        for i in messages.NICE_MESSAGES:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=i)
            time.sleep(1)
        if pidor_count == 1:
            congratulations = messages.NICE_1_TIME
        if pidor_count == 10:
            congratulations = messages.NICE_10_TIMES
        if pidor_count == 50:
            congratulations = messages.NICE_50_TIMES
        if pidor_count == 100:
            congratulations = messages.NICE_100_TIMES
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    if congratulations != "":
        await context.bot.send_message(chat_id=update.effective_chat.id, text=congratulations)
        await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                       sticker=stickers.DRINK_CHAMPAGNE)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    statistics = get_pidor_stats(chat_id, 'stats')
    if statistics == 'Ни один пользователь не зарегистрирован, статистики нет':
        await context.bot.send_message(chat_id=update.effective_chat.id, text=statistics)
    else:
        usernames = []
        counts = []
        for item in statistics.items():
            try:
                user_info = await context.bot.get_chat_member(chat_id, item[0])
                user_full_name = user_info.user.full_name
                user_nickname = user_info.user.username
                set_full_name_and_nickname_in_db(chat_id, item[0], user_full_name, user_nickname)
                usernames.append(f'{user_full_name} ({user_nickname})')
            except telegram.error.BadRequest:
                user_full_name_from_db = get_full_name_from_db(chat_id, item[0])
                user_nickname_from_db = get_nickname_from_db(chat_id, item[0])
                usernames.append(f'{user_full_name_from_db} ({user_nickname_from_db})')
            counts.append(item[1])
        user_stats = dict(zip(usernames, counts))
        text_list = ['Результаты игры красавчик дня:']
        for j in dict(sorted(user_stats.items(), key=lambda sort_item: sort_item[1], reverse=True)).items():
            text_list.append(f'{j[0]}: {j[1]}')
        text = '\n'.join(text_list)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def pidor_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    statistics = get_pidor_stats(chat_id, 'pidor_stats')
    if statistics == 'Ни один пользователь не зарегистрирован, статистики нет':
        await context.bot.send_message(chat_id=update.effective_chat.id, text=statistics)
    else:
        usernames = []
        counts = []
        for item in statistics.items():
            try:
                user_info = await context.bot.get_chat_member(chat_id, item[0])
                user_full_name = user_info.user.full_name
                user_nickname = user_info.user.username
                set_full_name_and_nickname_in_db(chat_id, item[0], user_full_name, user_nickname)
                usernames.append(f'{user_info.user.full_name} ({user_info.user.username})')
            except telegram.error.BadRequest:
                user_full_name_from_db = get_full_name_from_db(chat_id, item[0])
                user_nickname_from_db = get_nickname_from_db(chat_id, item[0])
                usernames.append(f'{user_full_name_from_db} ({user_nickname_from_db})')
            counts.append(item[1])
        user_stats = dict(zip(usernames, counts))
        text_list = ['Результаты игры пидор дня:']
        for j in dict(sorted(user_stats.items(), key=lambda sort_item: sort_item[1], reverse=True)).items():
            text_list.append(f'{j[0]}: {j[1]}')
        text = '\n'.join(text_list)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def reset_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    keyboard = [[
        InlineKeyboardButton("Да", callback_data=f"resetstats Yes {chat_id}"),
        InlineKeyboardButton("Нет", callback_data=f"resetstats No {chat_id}"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Точно сбросить статистику? Вернуть её будет нельзя, "
                                    "все забудут, кто был красавчиком", reply_markup=reply_markup)


async def member_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    reg_member = update.message.left_chat_member.id
    try:
        user_info = await context.bot.get_chat_member(chat_id, reg_member)
        full_name = user_info.user.full_name
        nickname = user_info.user.username
        set_full_name_and_nickname_in_db(chat_id, reg_member, full_name, nickname)
    except telegram.error.BadRequest:
        full_name = get_full_name_from_db(chat_id, reg_member)
        full_name = str(reg_member)
    message = unreg_in_data(chat_id, reg_member)
    if message == 'Пользователь не найден':
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Мы не будем по нему скучать, '
                                                                              'ведь он не был в игре🤡')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'{full_name} c позором бежал, но статистика всё помнит')


async def percent_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    members = get_all_members(chat_id)
    stats_list = []
    for j in members:
        stats_list.append(get_user_percentage_nice_pidor(chat_id, j))
    sorted_stats_list = sorted(stats_list, key=lambda d: d['nice'])
    text_list = []
    for i in sorted_stats_list:
        try:
            user_info = await context.bot.get_chat_member(chat_id, i['member_id'])
            user_full_name = user_info.user.full_name
            user_nickname = user_info.user.username
            set_full_name_and_nickname_in_db(chat_id, i['member_id'], user_full_name, user_nickname)
            text_list.append(f"{user_full_name} ({user_nickname}) на {i['nice']}% красавчик и на "
                             f"{i['pidor']}% пидор")
        except telegram.error.BadRequest:
            user_full_name_from_db = get_full_name_from_db(chat_id, i['member_id'])
            user_nickname_from_db = get_nickname_from_db(chat_id, i['member_id'])
            text_list.append(f"{user_full_name_from_db} ({user_nickname_from_db}) на {i['nice']}% красавчик и на "
                             f"{i['pidor']}% пидор")
    text = '\n'.join(text_list)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def show_coefficients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    coefficients = get_chat_members_nice_coefficients(chat_id)
    text_list = ["Вероятности стать красавчиком:"]
    for k, v in coefficients.items():
        text_list.append(f"{k} - {v}%")
    text = '\n'.join(text_list)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def show_pidor_coefficients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    coefficients = get_chat_members_pidor_coefficients(chat_id)
    text_list = ["Вероятности стать пидором:"]
    for k, v in coefficients.items():
        text_list.append(f"{k} - {v}%")
    text = '\n'.join(text_list)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def switch_on_carmic_dices_in_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    keyboard = [[
        InlineKeyboardButton("Да", callback_data=f"carma Yes {chat_id}"),
        InlineKeyboardButton("Нет", callback_data=f"carma No {chat_id}"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Включить кармические кубики? Если они включены, у пидоров больше шансов стать "
                                    "красавчиками, а у красавчиков - стать пидорами", reply_markup=reply_markup)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
**Пидорские команды**

`/reg` \- Принять участие в ИГРЕ
`/pidor` \- Активировать поиск пидора
`/run` \- Активировать поиск КРАУСАВЧИКА
`/unreg` \- Выйти нахуй из игры
`/stats` \- Стата
`/pidorstats` \- Пидорская стата
`/resetstats` \- Нахуй стату
`/percentstats` \- Процентная стата
`/nicecoefficients` \- Коэффициенты стать КРАУСАВЧИКОМ
`/pidorcoefficients` \- Коэффициенты стать пидором
`/carmicdices` \- Вкл\выкл карамельных кубов

**Команды для работы с событиями**

`/events` \- Список событий созданный участником в рамках чата
`/eventcreate Название` \- Создать событие с названием\. В ответ придет ID названия в рамках которого можно совершать операции\. Автоматически делает создателя участником\.
Пример: `/eventcreate Заказчик охуел\. Послать нахуй 23 августа в 18:00`

`/eventupdate ID Название` \- Изменение текста в сообщении\.
Пример: `/eventupdate 5 Илюха охуел просто послать его нахуй`

`/eventdelete ID` \- Удаляет навсегда событие\. После удаления востановлению не понадлежит\. Также удаляет всех участников
Пример: `/eventdelete 2`
    """

    await update.message.reply_text(
        text=text,
        parse_mode="MarkdownV2"
    )
    pass

# Обработчик ошибок
async def error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    chat_id = os.getenv('DEVELOPERT_CHAT_ID')
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "An exception was raised while handling an update\n"
            "<b>Update</b>\n"
            f"<pre>{html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n\n"
        ), parse_mode=ParseMode.HTML
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "<b>Context Chat</b>\n"
            f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        ), parse_mode=ParseMode.HTML
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "<b>Context User</b>\n"
            f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        ), parse_mode=ParseMode.HTML
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "<b>Trace</b>\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        ), parse_mode=ParseMode.HTML
    )

if __name__ == '__main__':
    application = (
        ApplicationBuilder()
        .token(os.getenv('BOT_TOKEN'))
        .read_timeout(10)
        .write_timeout(10)
        .connect_timeout(5)
        .pool_timeout(10)
        .build()
    )

    reg_handler = CommandHandler('reg', reg)
    unreg_handler = CommandHandler('unreg', unreg)
    pidor_handler = CommandHandler('pidor', pidor)
    run_handler = CommandHandler('run', run)
    stats_handler = CommandHandler('stats', stats)
    pidor_stats_handler = CommandHandler('pidorstats', pidor_stats)
    reset_stats_handler = CommandHandler('resetstats', reset_stats)
    percent_stats_handler = CommandHandler('percentstats', percent_stats)
    nice_coefficients_handler = CommandHandler('nicecoefficients', show_coefficients)
    pidor_coefficients_handler = CommandHandler('pidorcoefficients', show_pidor_coefficients)
    switch_on_carmic_dices_in_chat_handler = CommandHandler('carmicdices', switch_on_carmic_dices_in_chat)

    application.add_handlers([
        # pird
        reg_handler,
        unreg_handler,
        pidor_handler,
        run_handler,
        stats_handler,
        pidor_stats_handler,
        reset_stats_handler,
        percent_stats_handler,
        nice_coefficients_handler,
        pidor_coefficients_handler,
        switch_on_carmic_dices_in_chat_handler,

        # events
        CommandHandler('events', events.events),
        CommandHandler('eventcreate', events.event_create),
        CommandHandler('eventupdate', events.event_update),
        CommandHandler('eventdelete', events.event_delete),
        CommandHandler('eventremind', events.event_delete),

        # help
        CommandHandler('help', help),

        # handle query from keyboard
        CallbackQueryHandler(keyboard_handle)
    ])

    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, member_left))

    application.add_error_handler(error)

    application.run_polling()
