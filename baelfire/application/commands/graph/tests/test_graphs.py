from tempfile import NamedTemporaryFile

from mock import patch
from pytest import fixture

from ..graph import Graph

EXAMPLE_REPORT = {
    '__main__.MyElo': {
        'aborted': False,
        'dependencies': {
            'baelfire.dependencies.file.FileDoesNotExists': {
                'builded': True,
                'filename': '/tmp/elo',
                'index': 0,
                'phase_validation': True,
                'should_build': False,
                'success': True
            },
            'baelfire.dependencies.task.TaskDependency': {
                'builded': True,
                'index': 1,
                'phase_validation': True,
                'should_build': False,
                'success': True,
                'task': '__main__.MySecondElo',
            },
            'baelfire.dependencies.file.FileChanged': {
                'builded': True,
                'filename': '/tmp/elo',
                'index': 0,
                'phase_validation': True,
                'should_build': True,
                'success': True,
            },
            'baelfire.dependencies.file.FileSomething': {
                'builded': True,
                'filename': '/tmp/elo',
                'index': 0,
                'phase_validation': True,
                'should_build': True,
                'success': False,
            },
            'baelfire.dependencies.dependency.AlwaysRebuild': {
                'builded': True,
                'filename': '/tmp/elo',
                'index': 0,
                'phase_validation': True,
                'should_build': True,
                'success': True,
            },
        },
        'dependencies_run': [
            'baelfire.dependencies.file.FileDoesNotExists',
            'baelfire.dependencies.task.TaskDependency'],
        'needtorun': False,
        'runned': False,
        'signal': None,
        'success': False},
    '__main__.MySecondElo': {
        'aborted': False,
        'dependencies': {},
        'dependencies_run': [],
        'needtorun': False,
        'runned': False,
        'signal': None,
        'success': False,
    },
    '__main__.Something': {
        'aborted': False,
        'dependencies': {},
        'dependencies_run': [],
        'needtorun': True,
        'runned': False,
        'signal': None,
        'success': False,
    },
    '__main__.Something2': {
        'aborted': False,
        'dependencies': {},
        'dependencies_run': [],
        'needtorun': True,
        'runned': True,
        'signal': None,
        'success': True,
    },
    'last_index': 2
}

EXPECTED_DOT_FILE = """\
digraph {
    "__main__.MyElo"[label="MyElo",fillcolor=white,style=filled,shape=octagon];
        "baelfire.dependencies.file.FileChanged"[label="FileChanged",fillcolor=yellow,shape=diamond,style=filled];
            "baelfire.dependencies.file.FileChanged" -> "__main__.MyElo";
        "baelfire.dependencies.file.FileDoesNotExists"[label="FileDoesNotExists",fillcolor=white,shape=diamond,style=filled];
            "baelfire.dependencies.file.FileDoesNotExists" -> "__main__.MyElo";
        "baelfire.dependencies.file.FileSomething"[label="FileSomething",fillcolor=white,shape=diamond,style=filled];
            "baelfire.dependencies.file.FileSomething" -> "__main__.MyElo";
            "__main__.MySecondElo" -> "__main__.MyElo";
    "__main__.MySecondElo"[label="MySecondElo",fillcolor=white,style=filled];
    "__main__.Something"[label="Something",fillcolor=red,style=filled];
    "__main__.Something2"[label="Something2",fillcolor=green,style=filled];
}
"""


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
