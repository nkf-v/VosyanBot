from src.models import *

class DBInit:
    def execute(self):
        db.evolve()
