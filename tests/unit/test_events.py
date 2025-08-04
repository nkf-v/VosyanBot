from datetime import datetime

import pytest

from unittest.mock import Mock, MagicMock, AsyncMock

from peewee import SqliteDatabase, Database
from telegram import Update, Message, Chat, constants, User
from src.presenters.commands.telegram import events, event_create, event_update
from src.models import Event, EventMember

MODELS = [Event, EventMember]

class TestEvents:
    test_db: Database

    @classmethod
    def setup_class(cls):
        cls.test_db = SqliteDatabase(':memory:')

        cls.test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        cls.test_db.connect()
        cls.test_db.create_tables(MODELS)

    @classmethod
    def teardown_class(cls):
        cls.test_db.drop_tables(MODELS)
        cls.test_db.close()

    @pytest.mark.asyncio
    async def test_get_events_command(self):
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

        mock_send_message = AsyncMock()
        context = AsyncMock()
        context.bot.send_message = mock_send_message

        await events(update, context)

        mock_send_message.assert_called_once_with(
            chat_id=1,
            text="Ты бездельник!"
        )

    @pytest.mark.asyncio
    async def test_create_command(self):
        # Создаем мок Update
        update = Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=datetime(2025, 1, 1, 12, 0, 0),
                text="/eventcreate Test event",
                chat=Chat(id=1, type=constants.ChatType.GROUP),
                from_user=User(
                    id=1,
                    first_name='Name',
                    is_bot=False,
                )
            )
        )

        mock_send_message = AsyncMock()
        context = AsyncMock()
        context.args = ['Test', 'event']
        context.bot.send_message = mock_send_message

        await event_create(update, context)

        mock_send_message.assert_called_once_with(
            chat_id=1,
            text=f"Событие сохранено.\nID: 1"
        )

    @pytest.mark.asyncio
    async def test_update_command(self):
        # Создаем мок Update
        update = Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=datetime(2025, 1, 1, 12, 0, 0),
                text="/eventupdate 1 Test",
                chat=Chat(id=1, type=constants.ChatType.GROUP),
                from_user=User(
                    id=1,
                    first_name='Name',
                    is_bot=False,
                )
            )
        )

        mock_send_message = AsyncMock()
        context = AsyncMock()
        context.args = ['1', 'Test']
        context.bot.send_message = mock_send_message

        await event_update(update, context)

        mock_send_message.assert_called_once_with(
            chat_id=1,
            text=f"Событие обновлено\n- ID: 1 - Test"
        )
