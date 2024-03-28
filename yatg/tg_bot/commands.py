from yatg.tg_bot.bot import TgBot


def get_updates():
    """
    Get updates from telegram
    """
    bot = TgBot.from_config()
    updates = bot.get_updates()
    for upd in updates:
        upd.save()


def send_message():
    pass
