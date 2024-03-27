"""
Command for getting updates from tg to db
"""
from yatg.commands.base import Command


class CommandGetUpdates(Command):

    def execute(self):
        print(f'Get updates with settings: {self.settings}')


if __name__ == '__main__':
    command = CommandGetUpdates()
    command.execute()
