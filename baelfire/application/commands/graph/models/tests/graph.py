from mock import MagicMock
from soktest import TestCase

from ..graph import Graph

PREFIX = 'baelfire.application.commands.graph.models.graph.'


class GraphTest(TestCase):

    def setUp(self):
        super().setUp()
        self.graph = Graph()

    def test_init(self):
        self.assertEqual(None, self.graph.datalog)

    def test_open(self):
        """Should open temporary file and write initial data to it."""
        self.graph.open()

        self.graph.datalog.seek(0)
        self.assertEqual(b'digraph {\n', self.graph.datalog.read())

    def test_close(self):
        """Should write ending data to datalog."""
        self.graph.open()
        self.graph.close()
        self.graph.datalog.seek(0)
        self.assertEqual(b'digraph {\n}\n', self.graph.datalog.read())

    def test_read_lastlog(self):
        """Should write lastlog data into .lastlog"""
        self.add_mock(PREFIX + 'TaskLogger')
        self.mocks['TaskLogger'].read.return_value = 'exampledata'

        self.graph.read_lastlog()

        self.assertEqual('exampledata', self.graph.lastlog)

    def test_write(self):
        """Should encode data with utf8 and writes it to datalog."""
        self.add_mock_object(self.graph, 'datalog')
        data = MagicMock()

        self.graph.write(data)

        data.encode.assert_called_once_with('utf-8')
        self.mocks['datalog'].write.assert_called_once_with(
            data.encode.return_value)

    def test_generate_png(self):
        """Should run dot application to generate png from datalog."""
        self.add_mock(PREFIX + 'Popen')
        self.add_mock('builtins.open')
        self.graph.datalog = MagicMock()

        self.graph.generate_png()

        self.graph.datalog.seek.assert_called_once_with(0)
        self.mocks['open'].assert_called_once_with(self.graph.filename, 'w')
        filepipe = self.mocks['open'].return_value
        self.mocks['Popen'].assert_called_once_with(
            ['dot', '-x', '-Tpng'],
            stdin=self.graph.datalog,
            stdout=filepipe)
        spp = self.mocks['Popen'].return_value
        spp.wait.assert_called_once_with()
        filepipe.close.assert_called_once_with()

    def test_generate_task_visualization(self):
        """Should write task visualization and its dependencies."""
        self.graph.open()
        self.add_mock(PREFIX + 'TaskVisualization')
        visualization = self.mocks['TaskVisualization'].return_value
        visualization.details.return_value = 'task'
        dependency = MagicMock()
        visualization.dependencies.return_value = [dependency]
        visualization.links.return_value = 'links'
        visualization.invoked.return_value = 'invoked'
        dependency.details.return_value = 'dependency'

        self.graph.generate_task_visualization({})

        self.graph.datalog.seek(0)
        self.assertEqual(
            b'digraph {\ntasklinksinvokeddependency', self.graph.datalog.read())

        self.graph.close()

    def test_call(self):
        self.add_mock_object(self.graph, 'open')
        self.add_mock_object(self.graph, 'read_lastlog')
        self.add_mock_object(self.graph, 'generate_task_visualization')
        self.add_mock_object(self.graph, 'close')
        self.add_mock_object(self.graph, 'generate_png')
        self.graph.lastlog = ['task']

        self.graph()
        self.mocks['open'].assert_called_once_with()
        self.mocks['read_lastlog'].assert_called_once_with()
        self.mocks[
            'generate_task_visualization'].assert_called_once_with('task')

        self.mocks['close'].assert_called_once_with()
        self.mocks['generate_png'].assert_called_once_with()
