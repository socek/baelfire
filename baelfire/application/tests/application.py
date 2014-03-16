from mock import MagicMock
from soktest import TestCase

from baelfire.application.application import run, Application
from baelfire.application.commands.command import Command

PREFIX = 'baelfire.application.application.'


class ExampleCommand(Command):

    def __init__(self):
        super().__init__('example')
        self.made = False

    def make(self):
        self.made = True


class RunTest(TestCase):

    def test_simple(self):
        """Should initalize and run the Application class"""
        self.add_mock(PREFIX + "Application")

        run()

        self.mocks['Application'].assert_called_once_with()
        self.mocks['Application'].return_value.assert_called_once_with()


class ApplicationTest(TestCase):

    def setUp(self):
        super().setUp()
        self.app = Application()

    def test_init(self):
        """Should gather options and commands"""
        self.assertEqual(
            [
                'Init',
                'RunTask'
            ],
            sorted(list(self.app.commands)))
        self.assertEqual({}, self.app.options)
        self.assertEqual(['log'], self.app.option_names)

    def test_gather_commands(self):
        """Should gather all commands and assign self as a application."""
        self.app.commands = {}
        self.app.gather_commands()

        command_key = 'Init'
        self.assertEqual(self.app, self.app.commands[command_key].application)

    def test_create_parser(self):
        """Should create argument parser and add all commands to it."""
        self.add_mock(PREFIX + 'ArgumentParser')

        self.app.create_parser()

        self.assertEqual(self.mocks['ArgumentParser'].return_value,
                         self.app.parser)

        self.assertEqual(
            4,
            self.mocks['ArgumentParser'].return_value.add_argument.call_count)

    def test_parse_command_line(self):
        """Should convert to dict parsed command line with removed unused
        command arguments."""
        self.app.parser = MagicMock()
        self.app.parser.parse_args.return_value.__dict__ = {
            'init': 'command',
            'log': 'option',
            'something': None,
        }
        self.app.parse_command_line()

        self.assertEqual({'init': 'command', 'log': 'option'}, self.app.args)

    def test_convert_options(self):
        """Should put into options command line arguments or False if not
        present"""
        self.app.args = {'log': 'mylog', 'something': 'else'}
        self.app.convert_options()

        self.assertEqual({'log': 'mylog'}, self.app.options)

    def test_run_command_or_print_help_print_help(self):
        """Should print help when no command specyfied."""
        self.app.args = {}
        self.app.parser = MagicMock()

        self.app.run_command_or_print_help()

        self.app.parser.print_help.assert_called_once_with()

    def test_run_command_or_print_help_run_command(self):
        """Should run command which is in .args"""
        cmd = ExampleCommand()
        self.app.args = {cmd.name: 'something'}
        self.app.add_command(cmd)
        self.app.raw_args = {}

        self.app.run_command_or_print_help()

        self.assertEqual(True, cmd.made)
        self.assertEqual('something', cmd.args)

    def test_call(self):
        """Should create parser, parse line command, convert options and run
        command"""
        self.add_mock_object(self.app, 'create_parser')
        self.add_mock_object(self.app, 'parse_command_line')
        self.add_mock_object(self.app, 'convert_options')
        self.add_mock_object(self.app, 'run_command_or_print_help')
        self.app()

        self.mocks['create_parser'].assert_called_once_with()
        self.mocks['parse_command_line'].assert_called_once_with()
        self.mocks['convert_options'].assert_called_once_with()
        self.mocks['run_command_or_print_help'].assert_called_once_with()
