import os
import sys
from argparse import ArgumentParser

from .commands.init.command import Init
from .commands.main.command import RunTask
from .commands.list.command import ListTasks, ListAllTasks, PathsList
from .commands.graph.command import GraphCommand
from .commands.actual_recipe.command import ActualRecipe
from baelfire.error import RecipeNotFoundError, CommandError


class Application(object):

    def __init__(self, recipe=None, prefix=''):
        self.commands = {}
        self.options = {}
        self.gather_options()
        self.gather_commands()
        self.recipe = recipe

    def gather_commands(self):
        self.add_command(Init())
        self.add_command(RunTask())
        self.add_command(ListTasks())
        self.add_command(GraphCommand())
        self.add_command(ListAllTasks())
        self.add_command(PathsList())
        self.add_command(ActualRecipe())

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

        if self.recipe is None:
            self.parser.add_argument(
                '-r', '--recipe', dest='recipe',
                help='Use this recipe.',
            )

    def parse_command_line(self):
        self.raw_args = vars(self.parser.parse_args())
        self.args = {}
        for key, value in self.raw_args.items():
            if not value in [None, False, []]:
                self.args[key] = value

    def convert_options(self):
        for option in self.option_names:
            self.options[option] = self.args.pop(option, False)

    def run_command_or_print_help(self):
        if len(self.args) > 0:
            commands = filter(
                lambda command: command in self.commands,
                list(self.args))

            # this line is to make "GraphCommand" run last
            commands = sorted(commands, reverse=True)

            for name in commands:
                self.commands[name](self.args[name], self.raw_args)
        else:
            self.parser.print_help()

    def add_acutal_path(self):
        sys.path.append(os.getcwd())

    def __call__(self):
        self.add_acutal_path()
        self.create_parser()
        self.parse_command_line()
        self.convert_options()
        try:
            self.run_command_or_print_help()
        except (RecipeNotFoundError,) as error:
            print(error)
        except CommandError as error:
            print(error)


def run():
    Application()()
