from soktest import TestCase

from ..command import RunTask

PREFIX = 'baelfire.application.commands.main.command.'


class RunTaskTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = RunTask()

    def test_get_recipe_not(self):
        """Should return None if no recipe in init file or command switch."""
        self.assertEqual(None, self.command.get_recipe())

    def test_get_recipe_from_initfile(self):
        """Should rerurn recipe from init file."""
        self.add_mock(PREFIX + 'InitFile')
        self.mocks['InitFile'].return_value.is_present.return_value = True

        recipe = self.mocks[
            'InitFile'].return_value.get_recipe.return_value.return_value
        self.assertEqual(recipe, self.command.get_recipe())
        recipe = self.mocks[
            'InitFile'].return_value.get_recipe.assert_called_once_with()
