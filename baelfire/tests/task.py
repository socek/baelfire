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
