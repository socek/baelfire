from mock import MagicMock
from soktest import TestCase

from ..command import Command, TriggeredCommand

PREFIX = 'baelfire.application.commands.command.'


class CommandTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = Command('one', 'two', three='3')
        self.command.raw_args = {}

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

    def test_get_recipe_not(self):
        """Should return None if no recipe in init file or command switch."""
        self.assertEqual(None, self.command.get_recipe())

    def test_get_recipe_from_command_line(self):
        """Should return recipe from module specifed by command."""
        self.command.raw_args = {'recipe': 'myrecipe'}
        self.add_mock(PREFIX + 'import_module')

        result = self.command.get_recipe()

        self.assertEqual(
            self.mocks['import_module'].return_value.recipe(), result)

        self.mocks['import_module'].assert_called_once_with('myrecipe')

    def test_get_recipe_from_initfile(self):
        """Should rerurn recipe from init file."""
        self.add_mock(PREFIX + 'InitFile')
        self.mocks['InitFile'].return_value.is_present.return_value = True

        recipe = self.mocks[
            'InitFile'].return_value.get_recipe.return_value.return_value
        self.assertEqual(recipe, self.command.get_recipe())
        recipe = self.mocks[
            'InitFile'].return_value.get_recipe.assert_called_once_with()


class ExampleTriggeredCommand(TriggeredCommand):

    def __init__(self):
        super().__init__('mycommand')
        self.made = False

    def make(self):
        self.made = True


class TriggeredCommandTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = ExampleTriggeredCommand()

    def test_init(self):
        """Should add action="store_true" to kwargs."""
        self.assertEqual(
            {
                'action': 'store_true',
                'dest': 'ExampleTriggeredCommand'
            },
            self.command.kwargs)

    def test_call_when_triggered(self):
        """Should run make when triggered."""
        self.command(True)
        self.assertEqual(True, self.command.made)

    def test_call_when_not_triggered(self):
        """Should do nothing when not triggered."""
        self.command(False)
        self.assertEqual(False, self.command.made)
