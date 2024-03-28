from yatg.storage.db import DB


class Options:

    def __init__(self):
        self.db = DB()

    @property
    def last_update_id(self):
        val = self.get_option('last_update_id')
        return val if val else 0

    def get_option(self, key):
        raw_value = self.db.select_one(
            """
            SELECT "value"
            FROM "Options"
            WHERE "key" = ?
            """,
            key
        )
        return raw_value
