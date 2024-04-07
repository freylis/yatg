import logging

from yatg.settings import Settings
from yatg.storage.options import Options
from yatg.tg_bot.updates import Update

from yatg.utils import requester


logger = logging.getLogger('yatg')


class TgBot:

    def __init__(self, token, bot_name):
        self._token = token
        self._bot_name = bot_name
        self.settings = Settings()
        self.options = Options()

    def get_updates(self):
        """
        Get telegram updates
        """
        raw_data = self.command(
            action='getUpdates',
            params={
                'offset': self.options.last_update_id,
            }
        )
        updates = []
        for update_data in raw_data['result']:
            updates.append(Update(update_data))
        return updates

    @classmethod
    def from_config(cls):
        """
        Initialize telegram bot by config
        """
        settings = Settings()
        return cls(token=settings.tgbot_token, bot_name=settings.tgbot_name)

    def send_message(self, text, chat_id):
        """
        Отправка сообщения от бота к пользователю
        """
        self.command(
            action='sendMessage',
            params={
                'chat_id': chat_id,
                'text': text,
            }
        )

    def command(self, action, params=None):
        """
        Execute `action` command in telegram
        """
        full_url = f'{self.settings.tgbot_url}bot{self.settings.tgbot_token}/{action}'
        response_data = requester.get(full_url, params=params)
        return response_data
