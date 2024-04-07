import json

from yatg.storage.db import DB
from yatg.storage import Options
from yatg.storage.users import User


class Queue:
    STATUS_NEW = 1
    STATUS_DONE = 2
    STATUS_UNKNOWN_COMMAND = 3
    STATUS_ERROR = 4
    CONTENT_TYPE = NotImplemented

    def __init__(self, data, pk=None):
        self.data = data
        self.pk = pk
        self.db = DB()
        self.options = Options()

    @property
    def external_id(self):
        raise NotImplementedError()

    @property
    def username(self):
        return self.data['message']['chat']['username']

    @property
    def user(self):
        user = User(self.username)
        return user

    def save(self):
        """
        Save queue item if it doesnt exists
        """
        # check update already exists
        update_exists = self.db.select_one(
            """
            SELECT TRUE
            FROM "Queue"
            WHERE
                "content_type" = ?
                AND "external_id" = ?
                AND "user_id" = ?
            """,
            self.CONTENT_TYPE,
            str(self.external_id),
            self.user.pk,
        )
        if update_exists:
            return

        self.db.query(
            """
            INSERT INTO "Queue" (
                "content_type", "external_id", "user_id", "body", "status"
            ) VALUES (?, ?, ?, ?, ?)
            """,
            self.CONTENT_TYPE,
            str(self.external_id),
            self.user.pk,
            json.dumps(self.data, ensure_ascii=False),
            self.STATUS_NEW,
        )
