"""
Command for getting updates from tg to db
"""
import logging

from yatg.commands.base import Command


logger = logging.getLogger('yatg')


class CommandInitialize(Command):

    def execute(self):
        logger.info(f'Initialize db')
        self.db.initialize_db()


if __name__ == '__main__':
    command = CommandInitialize()
    command.execute()
