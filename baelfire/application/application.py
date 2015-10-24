import logging

from argparse import ArgumentParser
from importlib import import_module
from logging import getLogger

from baelfire.application.commands.graph.graph import Graph
from baelfire.error import TaskNotFoundError

log = getLogger(__name__)


class Application(object):

    def __init__(self):
        self.args = {}

    def create_parser(self):
        self.parser = ArgumentParser()

        tasks = self.parser.add_argument_group(
            'Tasks',
            'Tasks related options',
        )

        tasks.add_argument(
            '-t',
            '--task',
            dest='task',
            help='Run this task.',
        )
        tasks.add_argument(
            '-g',
            '--graph',
            dest='graph',
            help='Draw task dependency graph.',
            action="store_true",
        )

        other = self.parser.add_argument_group(
            'Other',
            'Other useful options',
        )
        other.add_argument(
            '-r',
            '--graph-file',
            dest='graph_file',
            help='Draw graph from report file.',
        )

        log = self.parser.add_argument_group(
            'Logging:',
            'Logging related options.',
        )

        log.add_argument(
            '-l',
            '--log-level',
            dest='log_level',
            help='Log level',
            default='info',
            choices=[
                'debug',
                'info',
                'warning',
                'error',
                'critical',
            ]
        )

    def configure_logging(self, args):
        level = getattr(logging, args.log_level.upper())
        format = ' * %(levelname)s %(name)s: %(message)s *'
        logging.basicConfig(level=level, format=format)

    def run_command_or_print_help(self, args):
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
        args = self.parser.parse_args()
        self.configure_logging(args)
        self.run_command_or_print_help(args)


def run():
    Application().run()
