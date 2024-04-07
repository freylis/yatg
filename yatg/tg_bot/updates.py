import json

from yatg.storage import DB
from yatg.utils import logger
from yatg.tg_bot import plugins
from yatg.tg_bot.queue import Queue


class Update(Queue):
    CONTENT_TYPE = 1

    @property
    def external_id(self):
        """
        Get id from tg data
        """
        return str(self.data['update_id'])

    @property
    def command_text(self):
        return self.data['message']['text']

    def execute(self):
        """
        Execute this update
        """
        logger.info(f'Execute command {self.command_text!r}')
        plugin_cls = plugins.get_plugin(self.command_text)
        plugin = plugin_cls()
        plugin.activate(self)

    def save(self):
        """
        Save item to queue
        Save last update id
        """
        super().save()
        self.options.last_update_id = str(self.external_id)

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
            WHERE "status" = ?
            ORDER BY "id"
            LIMIT ?
            """,
            cls.STATUS_NEW,
            size,
        )
        for rec in recs:
            data = json.loads(rec[1])
            update = cls(
                data=data,
                pk=rec[0]
            )
            yield update
