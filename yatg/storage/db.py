import logging
import sqlite3

from yatg.settings import Settings


logger = logging.getLogger('yatg')


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

    def select_field(self, query, *args):
        rec = self.select_one(query, *args)
        return rec[0] if rec else None

    def execute(self, query, *args):
        """
        Execute any query

        Returns:
            sqlite3.Cursor
        """
        connection = sqlite3.connect(self.settings.db_path)
        cursor = connection.cursor()
        logger.debug(f'[dbq] {query}; args={args}')
        cursor.execute(query, args)
        recs = cursor.fetchall()
        logger.debug(f'[dbr] rows: {len(recs)}')
        connection.commit()
        return recs

    def initialize_db(self):
        logger.info('Initialize db')
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
                name TEXT NOT NULL UNIQUE,
                plugin_data TEXT
            )
            """
        )
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS "Queue" (
                id INTEGER PRIMARY KEY,
                content_type INTEGER NOT NULL,
                external_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                body TEXT NOT NULL,
                status INTEGER NOT NULL,

                FOREIGN KEY (user_id)
                    REFERENCES User(id)
            )
            """
        )
        self.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS queue_ctype_extid_uid
            ON Queue(content_type, external_id, user_id)
            """
        )
