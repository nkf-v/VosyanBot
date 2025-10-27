import typer
from typing_extensions import Annotated

from src.applications.events.create import CreateEvenParams
from src.applications.events.delete import EventDeleteParams
from src.applications.events.remind import EventRemindParams
from src.applications.events.update import EventUpdateParams
from src.infrastructure.containers.events import App
from src.infrastructure.telegram import User
from src.presenters.commands.telegram.presenters import EventListMessagePresenter, EventDetailTelegramMessagePresenter

cli_app = typer.Typer()

app = App()

app.wire(modules=[
    __name__,
    'src',
])


@cli_app.command()
def list(
    chat_id: Annotated[int, typer.Argument()],
    member_id: Annotated[int, typer.Argument()],
):
    getter = app.event_applications().get_event_list()

    presenter = EventListMessagePresenter()

    getter.execute(
        chat_id=chat_id,
        member_id=member_id,
        presenter=presenter,
    )

    typer.echo(presenter.present())


@cli_app.command()
def create(chat_id: int, member_id: int, name: str, text: str):
    creator = app.event_applications().create_event()

    params = CreateEvenParams(
        chat_id,
        member_id,
        name,
        text,
        User('cli', 'Cli')
    )

    presenter = EventDetailTelegramMessagePresenter()

    creator.execute(
        params=params,
        presenter=presenter
    )

    message, _ = presenter.present()

    typer.echo(message)


@cli_app.command()
def delete(event_id: int, chat_id: int, member_id: int):
    deleter = app.event_applications().delete_event()

    params = EventDeleteParams(
        event_id,
        chat_id,
        member_id
    )

    message = deleter.execute(params)

    typer.echo(message)


@cli_app.command()
def update(event_id: int, chat_id: int, member_id: int, name: str, text: str):
    updater = app.event_applications().update_event()

    params = EventUpdateParams(
        event_id,
        chat_id,
        member_id,
        name,
        text,
    )

    presenter = EventDetailTelegramMessagePresenter()

    updater.execute(params, presenter)

    message, _ = presenter.present()

    typer.echo(message)


@cli_app.command()
def remind(event_id: int, chat_id: int, member_id: int):
    reminder = app.event_applications().remind_event()

    params = EventRemindParams(
        event_id,
        chat_id,
        member_id,
    )

    presenter = EventDetailTelegramMessagePresenter()

    reminder.execute(params, presenter)

    message, _ = presenter.present()

    typer.echo(message)


if __name__ == "__main__":
    cli_app()
