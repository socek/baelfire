from mock import MagicMock
from mock import patch
from pytest import fixture
from pytest import raises
from pytest import yield_fixture

from baelfire.application.application import Application
from baelfire.application.application import run
from baelfire.error import TaskNotFoundError
from baelfire.task import Task


class ExampleTask(Task):

    def create_dependecies(self):
        pass

    def build(self):
        pass


class TestApplication(object):

    @fixture
    def app(self):
        return Application()

    @yield_fixture
    def parse_args(self, app):
        app.create_parser()
        with patch.object(app.parser, 'parse_args') as parse_args:
            yield parse_args

    @yield_fixture
    def import_task(self, app):
        with patch.object(app, 'import_task') as mock:
            yield mock

    def test_run_without_args(self, app, parse_args):
        with patch.object(app.parser, 'print_help') as print_help:
            args = MagicMock()
            args.task = None
            args.graph_file = False

            app.run_command_or_print_help(args)

            print_help.assert_called_once_with()

    def test_run_with_task(self, app, parse_args):
        args = MagicMock()
        args.task = (
            'baelfire.application.tests.test_application:ExampleTask'
        )
        args.graph = False
        with patch.object(ExampleTask, 'phase_build') as phase_build:
            with patch.object(ExampleTask, 'save_report') as save_report:
                app.run_command_or_print_help(args)

                save_report.assert_called_once_with()
                phase_build.assert_called_once_with()

    def test_run_with_bad_task(self, app, parse_args):
        args = MagicMock()
        args.task = (
            'baelfire.application.tests.test_application:BadTask'
        )
        with raises(TaskNotFoundError):
            app.run_command_or_print_help(args)

    def test_run_with_task_error(self, app, import_task, parse_args):
        task = import_task.return_value.return_value
        task.run.side_effect = RuntimeError

        args = MagicMock()
        with raises(RuntimeError):
            app.run_command_or_print_help(args)

        import_task.assert_called_once_with(args.task)

    def test_run(self):
        parser_patcher = patch.object(
            Application,
            'create_parser',
            autospec=True,
        )
        run_patcher = patch.object(Application, 'run_command_or_print_help')
        with parser_patcher as create_parser:
            args = MagicMock()
            args.log_level = 'info'

            def side_effect(self):
                self.parser = MagicMock()
                self.parser.parse_args.return_value = args
            create_parser.side_effect = side_effect
            with run_patcher as run_command_or_print_help:
                run()
                assert create_parser.call_count == 1
                run_command_or_print_help.assert_called_once_with(args)

    def test_task_with_grap(self, app, parse_args):
        args = MagicMock()
        args.task = (
            'baelfire.application.tests.test_application:ExampleTask'
        )
        with patch('baelfire.application.application.Graph') as graph:
            with patch.object(ExampleTask, 'phase_build') as phase_build:
                with patch.object(ExampleTask, 'save_report') as save_report:
                    app.run_command_or_print_help(args)

                    save_report.assert_called_once_with()
                    phase_build.assert_called_once_with()
                    graph.assert_called_once_with(save_report.return_value)
                    graph.return_value.render.assert_called_once_with()

    def test_graph_drawing(self, app, parse_args):
        args = MagicMock()
        args.task = False
        with patch('baelfire.application.application.Graph') as graph:
            app.run_command_or_print_help(args)

            graph.assert_called_once_with(args.graph_file)
            graph.return_value.render.assert_called_once_with()
