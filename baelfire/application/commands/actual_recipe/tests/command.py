from soktest import TestCase

from ..command import ActualRecipe


class ListTasksTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = ActualRecipe()
        self.add_mock_object(self.command, 'get_recipe')
        self.add_mock('builtins.print')

    def test_make(self):
        """.make should print recipe class full import path."""
        self.command.make()
        self.mocks['print'].assert_called_once_with('mock:MagicMock')
