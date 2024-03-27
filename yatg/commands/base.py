"""
Base class interface for commands
"""
import logging

from yatg.settings import Settings
from yatg.storage import Storage


logger = logging.getLogger('yatg')


class Command:

    def __init__(self):
        self.settings = Settings()
        self.storage = Storage()

    def execute(self):
        logger.info('Execute base command!')
        raise NotImplementedError
