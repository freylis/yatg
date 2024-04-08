from yatg.storage import DB


class Plugin:
    NAME = NotImplemented
    TITLE = NotImplemented
    ALIASES = set()

    def __init__(self):
        self.db = DB()

    @property
    def title(self):
        return self.TITLE if self.TITLE is not NotImplemented else self.NAME

    @classmethod
    def is_activate_plugin_command(cls, command):
        """
        Get first argument (command name)
        Check plugin name is commands[0] ?
        """
        return (
            command == cls.NAME
            or command in cls.ALIASES
        )

    @classmethod
    def is_my_command(cls, command):
        """
        Проверка, является ли переданная команда командой из текущего плагина
        """
        return False

    def activate(self, user):
        """
        Save to user command
        """
        # проверяем актуальность данных о плагине у текущего пользователя
        user.plugin.activate(self)

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
