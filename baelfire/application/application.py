# import os
# import sys
from argparse import ArgumentParser
from importlib import import_module
from logging import getLogger

from baelfire.error import TaskNotFoundError
from baelfire.application.commands.graph.graph import Graph

log = getLogger(__name__)


class Application(object):

    def __init__(self):
        self.args = {}

    def create_parser(self):
        self.parser = ArgumentParser()

        self.parser.add_argument(
            '-t',
            '--task',
            dest='task',
            help='Run this task.',
        )
        self.parser.add_argument(
            '-g',
            '--graph',
            dest='graph',
            help='Draw task dependency graph.',
            action="store_true",
        )
        self.parser.add_argument(
            '-r',
            '--graph-file',
            dest='graph_file',
            help='Draw graph from report file.',
        )

    def run_command_or_print_help(self):
        args = self.parser.parse_args()
        if args.task:
            task = self.import_task(args.task)()
            try:
                task.run()
                report_path = task.save_report()
            except:
                log.error('Error in %(report)s' % task.paths)
                raise
            if args.graph:
                Graph(report_path).render()
        elif args.graph_file:
            Graph(args.graph_file).render()
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
