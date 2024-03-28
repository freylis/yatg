import json

from yatg.storage import DB
from yatg.storage.users import User


class Update:
    STATUS_NEW = 1
    STATUS_DONE = 2
    STATUS_UNKNOWN_COMMAND = 3
    STATUS_ERROR = 4

    def __init__(self, data):
        self.data = data
        self.db = DB()

    @property
    def username(self):
        return self.data['message']['chat']['username']

    @property
    def user(self):
        user = User(self.username)
        return user

    def save(self):
        """
        1. Save message from bot to queue
        2. save last message id
        """
        self.db.query(
            """
            INSERT INTO "Queue" (
                "user_id", "body", "status"
            ) VALUES (?, ?, ?)
            """,
            self.user.pk,
            json.dumps(self.data, ensure_ascii=False),
            self.STATUS_NEW,
        )
