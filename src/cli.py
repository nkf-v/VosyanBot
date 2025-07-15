import typer
from applications import MemberRegistration, MemberRegistrationDto
from models import db
from repositories import (
    MemberRepository,
    StatsRepository,
    PidorStsatsRepository,
    CurrentNiceRepository,
    CurrentPidorRepository
)

app = typer.Typer()

registration = MemberRegistration(
    member_repository=MemberRepository(),
    stats_repository=StatsRepository(),
    pidor_stats_repository=PidorStsatsRepository(),
    current_nice_repository=CurrentNiceRepository(),
    current_pidor_repository=CurrentPidorRepository()
)

@app.command()
def hello(name: str = "World"):
    typer.echo(f"Hello, {name}!")

@app.command()
def reg(chat_id: int, member_id: int):
    message = registration.execute(
        params=MemberRegistrationDto(
            chat_id=chat_id,
            member_id=member_id,
            user_full_name="Cli",
            user_nickname="cli"
        )
    )
    typer.echo(message)

if __name__ == "__main__":
    try:
        db.connect()
        app()
    finally:    
        db.close()