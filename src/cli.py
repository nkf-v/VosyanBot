import time

import typer
import src.infrastructure.events.cli as events
import src.infrastructure.event_members.cli as event_members
from src.infrastructure.containers.events import App

cli_app = typer.Typer()
cli_app.add_typer(events.cli_app, name="events")
cli_app.add_typer(event_members.cli_app, name="event_member")

app = App()

app.wire(modules=[
    __name__,
    'src',
])

@cli_app.command()
def hello(name: str = "World"):
    typer.echo(f"Hello, {name}!")


@cli_app.command()
def sleep():
    while True:
        typer.echo("Sleeping...")
        time.sleep(60)
        pass

@cli_app.command()
def db_evolve():
    app.gateways().db_connect_factory().create().evolve()


if __name__ == "__main__":
    cli_app()
