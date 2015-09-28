# import os
# import sys
from argparse import ArgumentParser
from importlib import import_module
from logging import getLogger

# from .commands.init.command import Init
# from .commands.main.command import RunTask
# from .commands.list.command import ListTasks, ListAllTasks, PathsList
# from .commands.graph.command import GraphCommand
# from .commands.actual_recipe.command import ActualRecipe
from baelfire.error import TaskNotFoundError

log = getLogger(__name__)


class Application(object):

    def __init__(self):
        self.args = {}

    def create_parser(self):
        self.parser = ArgumentParser()

        self.parser.add_argument(
            '-t', '--task', dest='task',
            help='Run this task.',
        )

    def run_command_or_print_help(self):
        args = self.parser.parse_args()
        if args.task:
            task = self.import_task(args.task)()
            try:
                task.run()
                task.save_report()
            except:
                log.error('Error in %(report)s' % task.paths)
                raise
        else:
            self.parser.print_help()

    def import_task(self, package_url):
        """Returns task from url "some.url:klass" """
        url = package_url.split(':')
        module = import_module(url[0])
        try:
            return getattr(module, url[1])
        except AttributeError:
            raise TaskNotFoundError(package_url)

    def run(self):
        self.create_parser()
        self.run_command_or_print_help()


def run():
    Application().run()
