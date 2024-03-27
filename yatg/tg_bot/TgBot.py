import logging


logger = logging.getLogger('yatg')


class TgBot:
    BOT_NAME = 'yadtg_bot'

    def __init__(self, token, bot_name):
        self._token = token
        self._bot_name = bot_name

    @classmethod
    def from_config(cls):
        """
        Initialize telegram bot by config
        """
        logger.error(f'Not implemented `{cls.__name__}.from_string` method')
        return cls(token='invalid_token', bot_name='invalid_bot_name')
