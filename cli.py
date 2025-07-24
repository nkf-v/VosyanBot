import typer
import time

from src.applications.events.update import EventUpdate, EventUpdateParams
from src.applications.member_registr import MemberRegistration, MemberRegistrationDto
from src.applications.events.create import CreateEvenParams, CreateEvent
from src.applications.events.get_list import GetEventList
from src.applications.events.delete import EventDelete

from src.infrastructure.db_init import DBInit
from src.models import db
from src.repositories import (
    MemberRepository,
    StatsRepository,
    PidorStsatsRepository,
    CurrentNiceRepository,
    CurrentPidorRepository,
    EventRepository
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
def db_init():
    (DBInit()).execute()
    typer.echo('Success init')

@app.command()
def event_create(chat_id: int, member_id: int, text: str):
    creator = CreateEvent(
        repository=EventRepository()
    )
    message = creator.execute(
        params=CreateEvenParams(
            chat_id=chat_id,
            member_id=member_id,
            text=text
        )
    )
    typer.echo(message)

@app.command()
def events(chat_id: int, member_id: int):
    getter = GetEventList(
        repository=EventRepository()
    )
    messages = getter.execute(
        chat_id=chat_id,
        member_id=member_id,
    )
    typer.echo('\n'.join(messages))

@app.command()
def event_delete(event_id: int, chat_id: int, member_id: int):
    delete = EventDelete(
        repository=EventRepository()
    )
    message = delete.execute(
        event_id=event_id,
        chat_id=chat_id,
        member_id=member_id,
    )

    typer.echo(message)

@app.command()
def event_update(event_id: int, chat_id: int, member_id: int, text: str):
    update = EventUpdate(
        repository=EventRepository()
    )

    message = update.execute(EventUpdateParams(
        event_id=event_id,
        chat_id=chat_id,
        member_id=member_id,
        text=text
    ))

    typer.echo(message)

@app.command()
def sleep():
    while True:
        typer.echo("Sleeping...")
        time.sleep(60)
        pass

if __name__ == "__main__":
    try:
        db.connect()
        app()
    finally:    
        db.close()