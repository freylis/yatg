from yatg.storage.db import DB


class Options:

    def __init__(self):
        self.db = DB()

    @property
    def last_update_id(self):
        val = self.get_option('last_update_id')
        return val if val else 0

    @last_update_id.setter
    def last_update_id(self, value):
        """
        Save last update to db
        """
        self.set_option('last_update_id', value)

    def get_option(self, key):
        """
        Get option raw value

        Returns:
            str|None: key value or null
        """
        raw_value = self.db.select_one(
            """
            SELECT "value"
            FROM "Options"
            WHERE "key" = ?
            """,
            key
        )
        return raw_value

    def set_option(self, key, value):
        """
        Save option <key> with value <value>
        Rewrite option it exists
        """
        cur_rec = self.db.select_one(
            """
            SELECT TRUE
            FROM "Options"
            WHERE "key" = ?
            """,
            key
        )
        if cur_rec:
            self.db.query(
                """
                UPDATE "Options"
                SET "value" = ?
                WHERE "key" = ?
                """,
                str(value),
                str(key),
            )
            return
        self.db.query(
            """
            INSERT INTO "Options" ("key", "value")
            VALUES (?, ?)
            """,
            str(key),
            str(value),
        )
