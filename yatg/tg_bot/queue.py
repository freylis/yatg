import json
import functools

from yatg.storage.db import DB
from yatg.storage import Options
from yatg.storage.users import User
from yatg.utils import logger


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

    def __str__(self):
        return f'<Q: ct:{self.CONTENT_TYPE} id:{self.pk}>'

    @property
    def external_id(self):
        raise NotImplementedError()

    @property
    def username(self):
        return self.data['message']['chat']['username']

    @functools.cached_property
    def user(self):
        user = User(self.username)
        return user

    def execute(self):
        raise NotImplementedError()

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

    def complete(self, status=None):
        if not self.pk:
            return
        status = status if status is not None else self.STATUS_DONE
        logger.debug(f'Задача {self} завершается со статусом {status}')

        self.db.query(
            """
            UPDATE "Queue"
            SET "status" = ?
            WHERE "id" = ?
            """,
            status,
            self.pk,
        )

    @classmethod
    def get_packet(cls, size=10):
        """
        Get <size> updates with status=new
        """
        db = DB()
        recs = db.select(
            """
            SELECT "id", "body"
            FROM "Queue"
            WHERE
                "status" = ?
                AND "content_type" = ?
            ORDER BY "id"
            LIMIT ?
            """,
            cls.STATUS_NEW,
            cls.CONTENT_TYPE,
            size,
        )
        for rec in recs:
            data = json.loads(rec[1])
            update = cls(
                data=data,
                pk=rec[0]
            )
            yield update
