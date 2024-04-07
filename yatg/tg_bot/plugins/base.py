import datetime
import json

from yatg.storage import DB
from yatg.tg_bot.bot import TgBot


class Plugin:
    NAME = NotImplementedError
    ALIASES = set()

    def __init__(self):
        self.db = DB()

    @classmethod
    def is_current_plugin(cls, command):
        """
        Get first argument (command name)
        Check plugin name is commands[0] ?
        """
        return (
            command == cls.NAME
            or command in cls.ALIASES
        )

    def activate(self, update):
        """
        Save to user command
        """
        # проверяем актуальность данных о плагине у текущего пользователя
        user_plugin = PluginUser(update.user)
        user_plugin.validate_with(self)

    def get_command(self, command):
        return


class Command:

    def __init__(self, command):
        self.command = command
        self.parts = command.strip()

    @property
    def plugin_name(self):
        """
        Get plugin name from command
        """
        return self.parts[0] if self.parts else None


class PluginUser:
    DT_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, user):
        self.user = user
        self.plugin_data = user.user_data['plugin_data']

    @property
    def name(self):
        """
        Получить актуальное название текущего плагина
        """
        return self.plugin_data.get('name')

    @property
    def datetime(self):
        """
        Получить дату / время последней работы пользователя с его плагином
        """
        raw_dt = self.plugin_data.get('datetime')
        return datetime.datetime.strptime(raw_dt, self.DT_FORMAT) if raw_dt else None

    def validate_with(self, another_plugin):
        """
        Провалидировать существующие данные с данными текущего плагина
        """
        if (
            self.name
            and self.name != another_plugin.NAME
        ):
            self.plugin_data = {}

        # устанавливаем данные текущего плагина
        self.plugin_data.update({
            'name': another_plugin.NAME,
            'datetime': datetime.datetime.now().strftime(self.DT_FORMAT),
        })
        self.activate()

    def activate(self):
        self.user.db.execute(
            """
            UPDATE "User"
            SET "plugin_data" = ?
            WHERE "name" = ?
            """,
            json.dumps(self.plugin_data, ensure_ascii=False),
            self.user.username,
        )
