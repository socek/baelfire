import logging

from soktest import TestCase

from ..command import RunTask
from baelfire.task import Task
from baelfire.recipe import Recipe
from baelfire.error import OnlyOneTaskInARow
from baelfire.dependencys import AlwaysRebuild

PREFIX = 'baelfire.application.commands.main.command.'


class ExampleTask(Task):

    def __init__(self):
        super().__init__()
        self.made = 0

    def generate_dependencys(self):
        self.add_dependecy(AlwaysRebuild())

    def make(self):
        self.made += 1


class SecondTask(Task):

    def generate_dependencys(self):
        pass


class RunTaskTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = RunTask()
        self.command.raw_args = {}

    def test_gather_tasks(self):
        """Should gather the tasks and assign command line arguments."""
        recipe = Recipe()
        task = ExampleTask()
        recipe.add_task(task)
        secondtask = SecondTask()
        recipe.add_task(secondtask)

        self.command.args = ['/exampletask?data=test', '/secondtask']
        self.command.recipe = recipe

        self.command.gather_tasks()

        self.assertEqual([task, secondtask], self.command.run_list)
        self.assertEqual(task.kwargs, {'data': ['test']})
        self.assertEqual(secondtask.kwargs, {})

    def test_gather_tasks_fail(self):
        """Should raise error when one task is forced to run more then once."""
        recipe = Recipe()
        task = ExampleTask()
        recipe.add_task(task)

        self.command.args = [
            '/exampletask?data=one', '/exampletask?second=two']
        self.command.recipe = recipe

        self.assertRaises(OnlyOneTaskInARow, self.command.gather_tasks)

    def test_run_tasks(self):
        """Should run all the tasks from run_list, but only once."""
        recipe = Recipe()
        recipe.log.task_log.setLevel(logging.CRITICAL)
        task = ExampleTask()
        recipe.add_task(task)
        recipe.validate_dependencys()

        self.command.run_list = [task, task]

        self.command.run_tasks()

        self.assertEqual(1, task.made)

    def test_make(self):
        """Should get recipe, gather tasks and run them."""
        recipe = Recipe()
        recipe.log.task_log.setLevel(logging.CRITICAL)
        task = ExampleTask()
        recipe.add_task(task)
        recipe.validate_dependencys()

        self.command.args = ['/exampletask']
        self.command.recipe = recipe

        self.add_mock_object(self.command, 'get_recipe', return_value=recipe)
        self.command.make()

        self.assertEqual(1, task.made)
