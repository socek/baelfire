from soktest import TestCase

from ..command import GraphCommand

PREFIX = 'baelfire.application.commands.graph.command.'


class GraphCommandTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = GraphCommand()

    def test_init(self):
        self.assertEqual('GraphCommand',
                         self.command.name)
        self.assertEqual(('-g', '--graph'), self.command.args)
        self.assertEqual(
            {
                'action': 'store_true',
                'dest': 'GraphCommand',
                'help': 'Generate graph from last runned command.'
            },
            self.command.kwargs)

    def test_make(self):
        """Should init and run Graph class."""
        self.add_mock(PREFIX + 'Graph')

        self.command.make()

        self.mocks['Graph'].assert_called_once_with()
        self.mocks['Graph'].return_value.assert_called_once_with()
