import json
import random

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.applications.event_members.invite import EventMemberInvite, EventMemberInviteParams, EventMemberInvitePresenter
from src.applications.event_members.leave import EventMemberLeave, EventMemberLeaveParams, EventMemberLeavePresenter
from src.applications.events.delete import EventDelete, EventDeleteParams
from src.applications.events.remind import EventRemind, EventRemindParams
from src.db_functions import reset_stats_data, remove_chat_from_carmic_dices_in_db, add_chat_to_carmic_dices_in_db
from src.infrastructure.containers.events import App
from src.presenters.commands.telegram.presenters import EventDetailTelegramMessagePresenter


async def keyboard_handle(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
) -> None:
    chat_id = update.callback_query.message.chat_id
    member_id = update.callback_query.from_user.id
    username = update.callback_query.from_user.username
    full_name = update.callback_query.from_user.full_name

    query = update.callback_query.data

    if query.startswith('resetstats') and (query.split(" ")[1] == 'No'):
        await update.callback_query.edit_message_text(text='Правильный выбор 👍')
    elif query.startswith('resetstats') and (query.split(" ")[1] == 'Yes'):
        chat_id = int(query.split(" ")[2])
        reset_stats_data(chat_id)
        await update.callback_query.edit_message_text(text='Статистика очищена, начинаем с чистого листа🙈')
    elif query.startswith('carma') and (query.split(" ")[1] == 'No'):
        chat_id = query.split(" ")[2]
        remove_chat_from_carmic_dices_in_db(chat_id)
        await update.callback_query.edit_message_text(text='Кармические кубики отключены')
    elif query.startswith('carma') and (query.split(" ")[1] == 'Yes'):
        chat_id = query.split(" ")[2]
        add_chat_to_carmic_dices_in_db(chat_id)
        await update.callback_query.edit_message_text(text='Кармические кубики включены')
    else:
        data = json.loads(query)
        action = data.get('action')
        event_id = data.get('event_id')
        message = None
        keyboard = None
        refresh = False

        app = App()

        app.wire(modules=[
            __name__,
            'src',
        ])

        match action:
            case 'dice_roll':
                dice = data.get('dice')
                result = random.randint(1, dice)
                message = f'Твой результат d{dice} => {result}'
                await update.callback_query.edit_message_text(text=message)

                return

            case 'event_delete':
                params = EventDeleteParams(
                    event_id,
                    chat_id,
                    member_id,
                )

                delete: EventDelete = app.event_applications().delete_event()
                message = delete.execute(params)

            case 'event_remind':
                params = EventRemindParams(
                    event_id,
                    chat_id,
                    member_id,
                )

                result = EventDetailTelegramMessagePresenter()

                remind: EventRemind = app.event_applications().remind_event()
                remind.execute(params, result)

                message, keyboard = result.present()

            case 'event_invite':
                params = EventMemberInviteParams(
                    event_id,
                    chat_id,
                    member_id,
                    username,
                    full_name,
                )

                presenter = EventMemberInvitePresenter()

                invite: EventMemberInvite = app.event_member_applications().invite()
                invite.execute(params, presenter)

                message = presenter.present()

                refresh = presenter.is_refresh()

            case 'event_leave':
                params = EventMemberLeaveParams(
                    event_id,
                    chat_id,
                    member_id,
                )

                presenter = EventMemberLeavePresenter()

                leave: EventMemberLeave = app.event_member_applications().leave()
                leave.execute(params, presenter)

                message = presenter.present()

                refresh = presenter.is_refresh()

            case _:
                message = 'Что-то пошло не так. Попробуйте позже.'

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard is not None else None

        await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

        if refresh:
            params = EventRemindParams(
                event_id,
                chat_id,
                member_id,
            )

            result = EventDetailTelegramMessagePresenter()

            remind: EventRemind = app.event_applications().remind_event()
            remind.execute(params, result)

            message, keyboard = result.present()

            await update.callback_query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard))