import logging

from yatg.tg_bot.bot import TgBot


logger = logging.Logger('yatg')


def get_updates():
    """
    Get updates from telegram
    """
    bot = TgBot.from_config()
    updates = bot.get_updates()
    logger.info(f'Got {len(updates)} updates')
    for upd in updates:
        upd.save()


def send_message(message):
    """
    Отправка сообщения из бота к пользователю
    """

