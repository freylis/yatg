from yatg.storage import DB


class User:

    def __init__(self, username):
        self.username = username
        self.db = DB()
        self.user_data = self._get_user_data()

    @property
    def pk(self):
        return self.user_data['id']

    def _get_user_data(self):
        existing_user = self.db.select_one(
            """
            SELECT "id", "name"
            FROM "User"
            WHERE "name" = ?
            """,
            self.username,
        )
        if not existing_user:
            self.db.query(
                """
                INSERT INTO "User" ("name")
                VALUES (?)
                """,
                self.username,
            )
            return self._get_user_data()
        return {
            'id': existing_user[0],
            'username': existing_user[1],
        }
