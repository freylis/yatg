import uuid
import logging
import datetime

from yatg.utils import requester
from yatg.settings import Settings
from yatg.tg_bot import plugins
from yatg.tg_bot.queue import Queue


logger = logging.getLogger('yatg')


class Update(Queue):
    CONTENT_TYPE = 1

    @property
    def external_id(self):
        """
        Get id from tg data
        """
        return str(self.data['update_id'])

    @property
    def chat_id(self):
        return self.data['chat']['id']

    @property
    def command_text(self):
        return self.data['message']['text']

    def execute(self):
        """
        Execute this update
        """
        logger.info(f'Execute command {self.command_text!r}')

        current_plugin_name = self.user.plugin.name
        logger.debug(
            f'Found active plugin {current_plugin_name!r}' if current_plugin_name else
            'Not found active plugin'
        )
        plugin_cls = plugins.get_plugin(current_plugin_name or self.command_text)
        plugin = plugin_cls()
        plugin.activate(self.user)

        # если команда является активацией плагина, завершим работу
        if plugin.is_activate_plugin_command(self.command_text):
            MessageToUser.answer_for_update(
                message=f'Активирована утилита {plugin.title}',
                update=self,
            )
            self.complete()
            return

        # в найденном плагине ищем команду
        if not plugin.is_my_command(self.command_text):
            MessageToUser.answer_for_update(
                message=f'Команда {self.command_text!r} не найдена в утилите {plugin.title}',
                update=self,
            )
            self.complete_with_error(f'Unknown command {self.command_text!r} for plugin={plugin.NAME}')
            return

    def save(self):
        """
        Save item to queue
        Save last update id
        """
        super().save()
        self.options.last_update_id = str(self.external_id)


class MessageToUser(Queue):
    CONTENT_TYPE = 2

    def __init__(self, data, pk=None):
        super().__init__(data, pk=pk)
        self.settings = Settings()

    def execute(self):
        action = 'sendMessage'
        params = {
            'chat_id': self.chat_id,
            'text': self.text,
        }
        full_url = f'{self.settings.tgbot_url}bot{self.settings.tgbot_token}/{action}'
        requester.get(full_url, params=params)
        self.complete()

    @property
    def chat_id(self):
        return self.data['message']['chat']['id']

    @property
    def text(self):
        return self.data['message']['text']

    @property
    def external_id(self):
        return self.data['update_id']

    @classmethod
    def answer_for_update(cls, message, update):
        """
        Инициализируем отправку сообщения пользователю на основе ранее отправленного сообщения
        """
        data = {
            "update_id": str(uuid.uuid4()),
            "message": {
                "chat": update.data['message']['chat'],
                "date": datetime.datetime.now().timestamp(),
                "text": message,
            },
        }
        msg = cls(data)
        msg.save()
