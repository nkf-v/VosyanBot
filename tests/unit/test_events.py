from datetime import datetime

import pytest

from unittest.mock import Mock

from peewee import SqliteDatabase
from telegram import Update, Message, Chat, constants, User
from src.presenters.commands.telegram import events
from src.models import Event, EventMember

MODELS = [Event, EventMember]

@pytest.mark.asyncio
async def test_start_command():
    test_db = SqliteDatabase(':memory:')

    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)

    # ---

    # Создаем мок Update
    update = Update(
        update_id=1,
        message=Message(
            message_id=1,
            date=datetime(2025, 1, 1, 12, 0, 0),
            text="/events",
            chat=Chat(id=1, type=constants.ChatType.GROUP),
            from_user=User(
                id=1,
                first_name='Name',
                is_bot=False,
            )
        )
    )

    mock_send_message = Mock()
    context = Mock()
    context.bot.send_message = mock_send_message

    await events(update, context)

    mock_send_message.assert_called_once_with(
        chat_id=1,
        text="Ты бездельник!"
    )

    # ---

    test_db.drop_tables(MODELS)
    test_db.close()
