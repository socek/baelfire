from mock import patch
from os import path
from pytest import fixture
from tempfile import NamedTemporaryFile

from ..graph import Graph


def open_relative_file(filename):
    base = path.dirname(__file__)
    filename = path.join(base, filename)
    return open(filename, 'r')

EXAMPLE_REPORT = {
    '__main__.MyElo': {
        'aborted': False,
        'dependencies': [
            {
                'builded': True,
                'filename': '/tmp/elo',
                'index': 0,
                'phase_validation': True,
                'should_build': False,
                'success': True,
                'name': 'baelfire.dependencies.file.FileDoesNotExists',
            },
            {
                'builded': True,
                'index': 1,
                'phase_validation': True,
                'should_build': False,
                'success': True,
                'task': '__main__.MySecondElo',
                'name': 'baelfire.dependencies.task.TaskDependency',
            },
            {
                'builded': True,
                'filename': '/tmp/elo',
                'index': 2,
                'phase_validation': True,
                'should_build': True,
                'success': True,
                'name': 'baelfire.dependencies.file.FileChanged',
            },
            {
                'builded': True,
                'filename': '/tmp/elo',
                'index': 3,
                'phase_validation': True,
                'should_build': True,
                'success': False,
                'name': 'baelfire.dependencies.file.FileSomething',
            },
            {
                'builded': True,
                'filename': '/tmp/elo',
                'index': 4,
                'phase_validation': True,
                'should_build': True,
                'success': True,
                'name': 'baelfire.dependencies.dependency.AlwaysRebuild',
            },
        ],
        'needtorun': False,
        'runned': False,
        'signal': None,
        'success': False},
    '__main__.MySecondElo': {
        'aborted': False,
        'dependencies': [],
        'needtorun': False,
        'runned': False,
        'signal': None,
        'success': False,
    },
    '__main__.Something': {
        'aborted': False,
        'dependencies': [],
        'needtorun': True,
        'runned': False,
        'signal': None,
        'success': False,
    },
    '__main__.Something2': {
        'aborted': False,
        'dependencies': [],
        'needtorun': True,
        'runned': True,
        'signal': None,
        'success': True,
    },
    'last_index': 2
}

EXPECTED_DOT_FILE = open_relative_file('expected_dot_file.txt').read()


class TestGraph(object):

    @fixture
    def path(self):
        return '/tmp/my/report.yaml'

    @fixture
    def obj(self, path):
        return Graph(path)

    def test_generate_png_file(self, obj):
        with patch('baelfire.application.commands.graph.graph.Popen') as popen:
            obj.generate_png_file()

            popen.assert_called_once_with(
                [
                    'dot -Tpng graph.dot -o graph.png',
                ],
                shell=True,
            )
            popen.return_value.wait.assert_called_once_with()

    def test_read_report(self, obj, path):
        open_patcher = patch('baelfire.application.commands.graph.graph.open')
        load_patcher = patch('baelfire.application.commands.graph.graph.load')
        with open_patcher as mopen:
            with load_patcher as mload:
                obj.read_report()

                mopen.assert_called_once_with(path, 'r')
                mload.assert_called_once_with(mopen.return_value)

    def test_render(self, obj):
        with patch.object(obj, 'generate_dot_file') as generate_dot_file:
            with patch.object(obj, 'generate_png_file') as generate_png_file:

                obj.render()

                generate_dot_file.assert_called_once_with()
                generate_png_file.assert_called_once_with()

    def test_with_fake_report(self, obj):
        patcher_read_report = patch.object(obj, 'read_report')
        with patcher_read_report as read_report:
            read_report.return_value = EXAMPLE_REPORT

            obj.Config.dot_path = NamedTemporaryFile().name
            obj.generate_dot_file()

            data = open(obj.Config.dot_path, 'r').read()
            assert EXPECTED_DOT_FILE == data.replace('\t', '    ')
