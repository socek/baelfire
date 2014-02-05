from mock import MagicMock
from soktest import TestCase

from .recipe import ExampleRecipe
from baelfire.task import Task


class ExampleTask(Task):

    def __init__(self):
        super().__init__()
        self.dep_1 = MagicMock()
        self.dep_1.return_value = False
        self.dep_2 = MagicMock()
        self.dep_2.return_value = False
        self.dep_3 = MagicMock()
        self.dep_3.return_value = False

    def get_dependencys(self):
        return [self.dep_1, self.dep_2, self.dep_3]


class TaskTest(TestCase):

    def setUp(self):
        super().setUp()
        self.task = ExampleTask()

    def test_set_recipe(self):
        """Should set recipe to a task"""
        recipe = ExampleRecipe()
        self.task.set_recipe(recipe)

        self.assertEqual(recipe, self.task.recipe)

    def test_get_path_with_path(self):
        """Should return path which is in self.path"""
        task = ExampleTask()
        task.path = '/sometask'

        self.assertEqual('/sometask', task.get_path())

    def test_get_path_without_path(self):
        """Should return generated path from class name when self.path is
        None"""
        task = ExampleTask()

        self.assertEqual('/exampletask', task.get_path())

    def test_paths(self):
        """Should return paths object from recipe"""
        recipe = ExampleRecipe()
        recipe.paths = 'paths'
        self.task.set_recipe(recipe)

        self.assertEqual('paths', self.task.paths)

    def test_settings(self):
        """Should return settings object from recipe"""
        recipe = ExampleRecipe()
        recipe.settings = 'settings'
        self.task.set_recipe(recipe)

        self.assertEqual('settings', self.task.settings)

    def test_is_rebuild_needed_false(self):
        """Should return false, if no dependency returned false."""
        self.assertEqual(False, self.task.is_rebuild_needed())

    def test_is_rebuild_needed_true(self):
        """Should return false, if one or more dependency returned true."""
        self.task.dep_2.return_value = True
        self.assertEqual(True, self.task.is_rebuild_needed())

    def test_is_rebuild_error(self):
        """Should raise error, when no get_dependencys method specyfied."""
        task = Task()
        self.assertRaises(AttributeError, task.is_rebuild_needed)
