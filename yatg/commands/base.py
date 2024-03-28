"""
Base class interface for commands
"""
import logging

from yatg.settings import Settings
from yatg.storage import DB
from yatg import tg_bot


logger = logging.getLogger('yatg')


class Command:

    def __init__(self):
        self.settings = Settings()
        self.tg_bot = tg_bot
        self.db = DB()

    def execute(self):
        logger.info('Execute base command!')
        raise NotImplementedError
