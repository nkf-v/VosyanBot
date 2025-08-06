import typer
import time

from src.applications.event_members.invite import EventMemberInvite, EventMemberInviteParams
from src.applications.event_members.leave import EventMemberLeave, EventMemberLeaveParams
from src.applications.events.remind import EventRemindParams, EventRemind
from src.applications.events.update import EventUpdate, EventUpdateParams
from src.applications.members.registry import MemberRegistration, MemberRegistrationDto
from src.applications.events.create import CreateEvenParams, CreateEvent
from src.applications.events.get_list import GetEventList
from src.applications.events.delete import EventDelete, EventDeleteParams
from src.applications.members.unregister import MemberUnregister

from src.infrastructure.db_init import DBInit
from src.models import db
from src.repositories import (
    MemberRepository,
    StatsRepository,
    PidorStsatsRepository,
    CurrentNiceRepository,
    CurrentPidorRepository,
    EventRepository,
    EventMemberRepository
)

app = typer.Typer()

@app.command()
def hello(name: str = "World"):
    typer.echo(f"Hello, {name}!")

@app.command()
def reg(chat_id: int, member_id: int):
    registration = MemberRegistration(
        member_repository=MemberRepository(),
        stats_repository=StatsRepository(),
        pidor_stats_repository=PidorStsatsRepository(),
        current_nice_repository=CurrentNiceRepository(),
        current_pidor_repository=CurrentPidorRepository()
    )

    message = registration.execute(
        params=MemberRegistrationDto(
            chat_id=chat_id,
            member_id=member_id,
            user_full_name="Cli",
            user_nickname="cli"
        )
    )
    typer.echo(message)

@app.command()
def unreg(chat_id: int, member_id: int):
    unreg = MemberUnregister(
        repository=MemberRepository()
    )
    message = unreg.execute(chat_id, member_id)
    typer.echo(message)

@app.command()
def db_init():
    (DBInit()).execute()
    typer.echo('Success init')

@app.command()
def event_create(chat_id: int, member_id: int, text: str):
    creator = CreateEvent(
        event_repository=EventRepository(),
        event_member_repository=EventMemberRepository()
    )
    message = creator.execute(
        params=CreateEvenParams(
            chat_id,
            member_id,
            text,
            'cli',
            'cli'
        )
    )
    typer.echo(message)

@app.command()
def events(chat_id: int, member_id: int):
    getter = GetEventList(
        repository=EventRepository(),
        event_member_repository=EventMemberRepository()
    )
    messages = getter.execute(
        chat_id=chat_id,
        member_id=member_id,
    )
    typer.echo('\n'.join(messages))

@app.command()
def event_delete(event_id: int, chat_id: int, member_id: int):
    delete = EventDelete(
        repository=EventRepository(),
        event_member_repository=EventMemberRepository()
    )

    params = EventDeleteParams(
        event_id,
        chat_id,
        member_id
    )

    message = delete.execute(params)

    typer.echo(message)

@app.command()
def event_update(event_id: int, chat_id: int, member_id: int, text: str):
    update = EventUpdate(
        repository=EventRepository()
    )

    params = EventUpdateParams(
        event_id,
        chat_id,
        member_id,
        text
    )

    message = update.execute(params)

    typer.echo(message)

@app.command()
def event_remind(event_id: int, chat_id: int, member_id: int):
    remind = EventRemind(
        event_repository=EventRepository(),
        event_member_repository=EventMemberRepository()
    )

    params = EventRemindParams(
        event_id,
        chat_id,
        member_id,
    )

    message = remind.execute(params)

    typer.echo(message)

@app.command()
def event_invite(event_id: int, chat_id: int, member_id: int):
    invite = EventMemberInvite(
        event_repository=EventRepository(),
        event_member_repository=EventMemberRepository()
    )

    params = EventMemberInviteParams(
        event_id,
        chat_id,
        member_id,
        'cli',
        'cli'
    )

    message = invite.execute(params)

    typer.echo(message)

@app.command()
def event_leave(event_id: int, chat_id: int, member_id: int):
    leave = EventMemberLeave(
        event_repository=EventRepository(),
        event_member_repository=EventMemberRepository()
    )

    params = EventMemberLeaveParams(
        event_id,
        chat_id,
        member_id,
    )

    message = leave.execute(params)

    typer.echo(message)

@app.command()
def sleep():
    while True:
        typer.echo("Sleeping...")
        time.sleep(60)
        pass

if __name__ == "__main__":
    try:
        db.connect(reuse_if_open=True)
        app()
    finally:    
        db.close()