import typer

from src.applications.event_members.invite import EventMemberInviteParams
from src.applications.event_members.leave import EventMemberLeaveParams
from src.infrastructure.containers.events import App

cli_app = typer.Typer()

app = App()

app.wire(modules=[
    __name__,
    'src',
])


@cli_app.command()
def invite(event_id: int, chat_id: int, member_id: int):
    invite = app.event_member_applications().invite()

    params = EventMemberInviteParams(
        event_id,
        chat_id,
        member_id,
        'cli',
        'cli'
    )

    message = invite.execute(params)

    typer.echo(message)


@cli_app.command()
def leave(event_id: int, chat_id: int, member_id: int):
    leave = app.event_member_applications().leave()

    params = EventMemberLeaveParams(
        event_id,
        chat_id,
        member_id,
    )

    message = leave.execute(params)

    typer.echo(message)

if __name__ == "__main__":
    cli_app()
