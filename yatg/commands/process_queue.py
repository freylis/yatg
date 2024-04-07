"""
Command for getting updates from tg to db
"""
from yatg.commands.base import Command

from yatg.tg_bot.updates import Update


class ProcessQueueCommand(Command):

    def execute(self):
        """
        1. get N-new items from queue
        2. Execute each command
        """
        updates_packet = Update.get_packet()
        for update in updates_packet:
            update.execute()


if __name__ == '__main__':
    command = ProcessQueueCommand()
    command.execute()
