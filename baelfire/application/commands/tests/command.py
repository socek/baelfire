from mock import MagicMock
from soktest import TestCase

from ..command import Command


class CommandTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = Command('one', 'two', three='3')

    def test_init(self):
        self.assertEqual(
            'Command', self.command.name)
        self.assertEqual(('one', 'two'), self.command.args)
        self.assertEqual(
            {
                'three': '3',
                'dest': 'Command'
            },
            self.command.kwargs)

    def test_assign_argument(self):
        """Should user parser to add command argument with .args and .kwargs"""
        parser = MagicMock()
        self.command.assign_argument(parser)

        parser.add_argument.assert_called_once_with(
            'one',
            'two',
            three='3',
            dest='Command')

    def test_assign_application(self):
        """Should assign parent application"""
        app = MagicMock()

        self.command.assign_application(app)

        self.assertEqual(app, self.command.application)

    def test_call(self):
        """Should assign args and run make (or raise error on missing make)"""

        self.assertRaises(AttributeError, self.command, 'args')

        self.assertEqual('args', self.command.args)
