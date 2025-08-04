from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from peewee import SqliteDatabase, Database
from telegram import Update, Message, Chat, constants, User, ChatMember

from src.models import Event, EventMember
from src.presenters.commands.telegram.events import events, event_create, event_update, event_delete, event_remind

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

    def create_user(self):
        return User(
            id=1,
            first_name='First',
            last_name='Last',
            is_bot=False,
            username='name',

        )

    def create_context(self, args):
        get_chat_member_mock = AsyncMock()
        get_chat_member_mock.return_value = ChatMember(user=self.create_user(), status=ChatMember.MEMBER)

        mock_send_message = AsyncMock()
        context = AsyncMock()
        context.args = args
        context.bot.send_message = mock_send_message
        context.bot.get_chat_member = get_chat_member_mock

        return context, mock_send_message

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
                from_user=self.create_user()
            )
        )

        context, mock = self.create_context([])

        await events(update, context)

        mock.assert_called_once_with(
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
                from_user=self.create_user()
            )
        )

        context, mock = self.create_context(['Test event'])

        await event_create(update, context)

        mock.assert_called_once_with(
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
                from_user=self.create_user()
            )
        )

        context, mock = self.create_context(['1', 'Test'])

        await event_update(update, context)

        mock.assert_called_once_with(
            chat_id=1,
            text=f"Событие обновлено\n- ID: 1 - Test"
        )

    @pytest.mark.asyncio
    async def test_remind_command(self):
        # Создаем мок Update
        update = Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=datetime(2025, 1, 1, 12, 0, 0),
                text="/eventremind 1",
                chat=Chat(id=1, type=constants.ChatType.GROUP),
                from_user=self.create_user()
            )
        )

        context, mock = self.create_context(['1'])

        await event_remind(update, context)

        mock.assert_called_once_with(
            chat_id=1,
            text='\n'.join([
                'Событие:',
                f"- ID 1 - Test",
                '',
                'Участники:',
                '- First Last (@name)',
            ])
        )

    @pytest.mark.asyncio
    async def test_delete_command(self):
        # Создаем мок Update
        update = Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=datetime(2025, 1, 1, 12, 0, 0),
                text="/eventdelete 1",
                chat=Chat(id=1, type=constants.ChatType.GROUP),
                from_user=self.create_user()
            )
        )

        context, mock = self.create_context(['1'])

        await event_delete(update, context)

        mock.assert_called_once_with(
            chat_id=1,
            text='Событие удалено'
        )