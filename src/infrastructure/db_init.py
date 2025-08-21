from src.models import *

class DBInit:
    def execute(self):
        db.connect(reuse_if_open=True)
        db.evolve()
        db.close()
