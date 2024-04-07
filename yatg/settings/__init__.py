import os
import yaml

from yatg import utils


class Settings:

    def __init__(self):
        self._options = self._read_all()

    def __str__(self):
        return f'<Settings {self.path!r}>'

    @property
    def db_path(self):
        path = self.get_option('db', 'fullpath')
        path = os.path.abspath(path)
        return path

    @property
    def tgbot_token(self):
        """
        Token by path `tgbot / token`
        """
        tkn = self._get_tgbot_option('token')
        return tkn

    @property
    def tgbot_name(self):
        """
        Get telegram bot name
        """
        return self._get_tgbot_option('name')

    @property
    def tgbot_url(self):
        """
        Get url to telegram-api
        """
        return self._get_tgbot_option('api_url')

    @property
    def tgbot_plugins(self):
        """
        Get paths to plugins
        """
        return self._get_tgbot_option('plugins')

    def get_option(self, *keys):
        """
        Get option by path
        Args:
            *keys: keys for option getting

        Returns:
            any
        """
        options = self._options

        if not keys:
            return None

        value = None
        while keys:
            key = keys[0]
            value = options.get(key)
            if value is None:
                raise utils.InvalidOptionError(f'You should define {" / ".join(keys)!r} option')

            options = value
            keys = keys[1:]

        return value

    @property
    def path(self):
        """
        Returns:
            str: config file path
        """
        return os.path.join(os.getcwd(), 'yatg.settings.yaml')

    def _read_all(self):
        with open(self.path, 'rb') as file:
            full = yaml.safe_load(file)
        return full

    def _get_tgbot_option(self, key):
        """
        Get option from section `tgbot`
        """
        return self.get_option('tgbot', key)