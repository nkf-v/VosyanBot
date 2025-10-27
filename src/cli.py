import time

import typer
import src.infrastructure.events.cli as events
import src.infrastructure.event_members.cli as event_members

cli_app = typer.Typer()
cli_app.add_typer(events.cli_app, name="events")
cli_app.add_typer(event_members.cli_app, name="event_member")

@cli_app.command()
def hello(name: str = "World"):
    typer.echo(f"Hello, {name}!")


@cli_app.command()
def sleep():
    while True:
        typer.echo("Sleeping...")
        time.sleep(60)
        pass

if __name__ == "__main__":
    cli_app()
