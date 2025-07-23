from src.models import Event, CarmicDicesEnabled, CurrentNice, CurrentPidor, Stats, PidorStats, Member


class DBInit:
    def execute(self):
        Member.create_table()
        PidorStats.create_table()
        Stats.create_table()
        CurrentPidor.create_table()
        CurrentNice.create_table()
        CarmicDicesEnabled.create_table()
        Event.create_table()