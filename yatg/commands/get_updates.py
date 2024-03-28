"""
Command for getting updates from tg to db
"""
from yatg.commands.base import Command

from yatg.tg_bot import get_updates


class CommandGetUpdates(Command):

    def execute(self):
        get_updates()


if __name__ == '__main__':
    command = CommandGetUpdates()
    command.execute()
