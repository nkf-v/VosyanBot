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
        mock_send_message = AsyncMock()
        context = AsyncMock()
        context.args = args
        context.bot.send_message = mock_send_message

        return context, mock_send_message

    @pytest.mark.asyncio
    async def test_get_empty_events_command(self):
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
            text="🤡 Ты бездельник!"
        )

    @pytest.mark.asyncio
    async def test_create_command(self):
        mock_reply_text = AsyncMock()

        mock_message = AsyncMock()
        mock_message.message_id = 1
        mock_message.date = datetime(2025, 1, 1, 12, 0, 0)
        mock_message.text = "/events"
        mock_message.chat = Chat(id=1, type=constants.ChatType.GROUP)
        mock_message.from_user = self.create_user()
        mock_message.reply_text = mock_reply_text

        update = Update(
            update_id=1,
            message=mock_message,
        )

        context, mock = self.create_context(['Test event'])

        await event_create(update, context)

        mock_reply_text.assert_called_once_with(
            text='\n'.join([
                'Событие:',
                "- ID 1 - Test event",
                '',
                'Участники:',
                '- First Last (@name)',
            ])
        )


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
            text='🎉 Твои ни никому не нужные события:\nID: 1 - Test event'
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