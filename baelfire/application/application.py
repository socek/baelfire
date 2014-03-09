from argparse import ArgumentParser

from .commands.init.command import Init
from .commands.main.command import RunTask


class Application(object):

    def __init__(self):
        self.commands = {}
        self.options = {}
        self.gather_options()
        self.gather_commands()

    def gather_commands(self):
        self.add_command(Init())
        self.add_command(RunTask())

    def gather_options(self):
        self.option_names = [
            'log',
        ]

    def add_command(self, command):
        command.assign_application(self)
        self.commands[command.name] = command

    def create_parser(self):
        self.parser = ArgumentParser()
        for name, command in self.commands.items():
            command.assign_argument(self.parser)

        self.parser.add_argument(
            '-l', '--log', dest='log', action='store_true',
            help='Set log level from "debug" or "info".')

    def parse_command_line(self):
        args = vars(self.parser.parse_args())
        self.args = {}
        for key, value in args.items():
            if value is not None:
                self.args[key] = value

    def convert_options(self):
        for option in self.option_names:
            self.options[option] = self.args.pop(option, False)

    def run_command_or_print_help(self):
        if len(self.args) > 0:
            for name, value in self.args.items():
                self.commands[name](value)
        else:
            self.parser.print_help()

    def __call__(self):
        self.create_parser()
        self.parse_command_line()
        self.convert_options()
        self.run_command_or_print_help()


def run():
    Application()()
