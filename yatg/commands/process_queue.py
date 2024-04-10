"""
Command for getting updates from tg to db
"""
import time

from yatg.commands.base import Command
from yatg.tg_bot.updates import Update
from yatg.tg_bot.updates import MessageToUser


class ProcessQueueCommand(Command):

    def execute(self):
        """
        1. get N-new items from queue
        2. Execute each command
        """
        for cls in [Update, MessageToUser]:
            queue = cls.get_packet()
            for q_item in queue:
                q_item.execute()


if __name__ == '__main__':
    command = ProcessQueueCommand()
    while True:
        try:
            command.execute()
        except KeyboardInterrupt:
            logger.warning(f'Stop command {command}')
            break

        time.sleep(1)
