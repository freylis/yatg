import sqlite3

from yatg.settings import Settings


class DB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.settings = Settings()
        self._db_file = self.settings.db_path

    def query(self, query, *args):
        self.execute(query, *args)
        return None

    def select(self, query, *args):
        return self.execute(query, *args)

    def select_one(self, query, *args):
        recs = self.select(query, *args)
        return recs[0] if recs else None

    def execute(self, query, *args):
        """
        Execute any query

        Returns:
            sqlite3.Cursor
        """
        connection = sqlite3.connect(self.settings.db_path)
        cursor = connection.cursor()
        cursor.execute(query, args)
        recs = cursor.fetchall()
        connection.commit()
        return recs

    def initialize_db(self):
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS "Options" (
                id INTEGER PRIMARY KEY,
                key TEXT NOT NULL,
                value TEXT NOT NULL
            )
            """
        )
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS "User" (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
            """
        )
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS "Queue" (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                body TEXT NOT NULL,
                status INTEGER NOT NULL,

                FOREIGN KEY (user_id)
                    REFERENCES User(id)
            )
            """
        )
