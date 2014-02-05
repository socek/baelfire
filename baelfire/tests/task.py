from soktest import TestCase

from .recipe import ExampleRecipe
from baelfire.task import Task


class ExampleTask(Task):
    pass


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
