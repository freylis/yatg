import json
import datetime

from yatg.storage import DB


class User:

    def __init__(self, username):
        self.username = username
        self.db = DB()
        self.user_data = self._get_user_data()
        self.plugin = PluginData(self)

    @property
    def pk(self):
        return self.user_data['id']

    def _get_user_data(self):
        existing_user = self.db.select_one(
            """
            SELECT "id", "name", "plugin_data"
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
            'plugin_data': json.loads(existing_user[2] or '{}')
        }


class PluginData:
    DT_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, user):
        self.user = user
        self.plugin_data = user.user_data['plugin_data']

    @property
    def name(self):
        return self._get_plugin_field('name')

    @property
    def datetime(self):
        raw_dt = self._get_plugin_field('datetime')
        return datetime.datetime.strptime(raw_dt, self.DT_FORMAT) if raw_dt else None

    def _get_plugin_field(self, field):
        return self.plugin_data.get(field)

    def activate(self, plugin):
        self.plugin_data.update({
            'name': plugin.NAME,
            'datetime': datetime.datetime.now().strftime(self.DT_FORMAT)
        })

        self.user.db.execute(
            """
            UPDATE "User"
            SET "plugin_data" = ?
            WHERE "name" = ?
            """,
            json.dumps(self.plugin_data, ensure_ascii=False),
            self.user.username,
        )
