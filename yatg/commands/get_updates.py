"""
Command for getting updates from tg to db
"""
import time
import logging
from yatg.commands.base import Command

from yatg.tg_bot import get_updates


logger = logging.getLogger('yatg')


class CommandGetUpdates(Command):

    def execute(self):
        get_updates()


if __name__ == '__main__':
    command = CommandGetUpdates()
    logger.info('logger works!')
    print('w!')
    while True:
        command.execute()
        time.sleep(1)
