from argparse import ArgumentParser

from .commands.init.command import Init
from .commands.main.command import RunTask
from .commands.list.command import ListTasks
from baelfire.error import RecipeNotFoundError, CommandAborted, CommandError


class Application(object):

    def __init__(self):
        self.commands = {}
        self.options = {}
        self.gather_options()
        self.gather_commands()

    def gather_commands(self):
        self.add_command(Init())
        self.add_command(RunTask())
        self.add_command(ListTasks())

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
            '-r', '--recipe', dest='recipe',
            help='Use this recipe.',
        )

    def parse_command_line(self):
        self.raw_args = vars(self.parser.parse_args())
        self.args = {}
        for key, value in self.raw_args.items():
            if value is not None:
                self.args[key] = value

    def convert_options(self):
        for option in self.option_names:
            self.options[option] = self.args.pop(option, False)

    def run_command_or_print_help(self):
        if len(self.args) > 0:
            commands = filter(
                lambda command: command[0] in self.commands,
                self.args.items())
            for name, value in commands:
                self.commands[name](value, self.raw_args)
        else:
            self.parser.print_help()

    def __call__(self):
        self.create_parser()
        self.parse_command_line()
        self.convert_options()
        try:
            self.run_command_or_print_help()
        except (RecipeNotFoundError,) as error:
            print(error)
        except CommandAborted:
            print('\r >> Command aborted!')
        except CommandError as error:
            print(error)


def run():
    Application()()
