import sqlite3
from yatg.storage.initializer import initialize_db


class DB:

    def __init__(self):
        self.db = initialize_db()


class Storage:

    def __init__(self):
        self.db = DB()
