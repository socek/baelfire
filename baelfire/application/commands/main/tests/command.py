import logging
from mock import MagicMock

from soktest import TestCase

from ..command import RunTask
from baelfire.task import Task
from baelfire.recipe import Recipe
from baelfire.dependencies import AlwaysRebuild
from baelfire.error import OnlyOneTaskInARowError, CommandAborted

PREFIX = 'baelfire.application.commands.main.command.'


class ExampleTask(Task):

    def __init__(self):
        super().__init__()
        self.made = 0

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def make(self):
        self.made += 1


class SecondTask(Task):

    def generate_dependencies(self):
        pass


class RunTaskTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = RunTask()
        self.command.raw_args = {}

    def test_gather_tasks(self):
        """Should gather the tasks and assign command line arguments."""
        recipe = Recipe()
        recipe.add_task(ExampleTask)
        task = recipe.task_from_url('/exampletask')
        recipe.add_task(SecondTask)
        secondtask = recipe.task_from_url('/secondtask')

        self.command.args = ['/exampletask?data=test', '/secondtask']
        self.command.recipe = recipe

        self.command.gather_tasks()

        self.assertEqual([task, secondtask], self.command.run_list)
        self.assertEqual(task.kwargs, {'data': ['test']})
        self.assertEqual(secondtask.kwargs, {})

    def test_gather_tasks_fail(self):
        """Should raise error when one task is forced to run more then once."""
        recipe = Recipe()
        recipe.add_task(ExampleTask)

        self.command.args = [
            '/exampletask?data=one', '/exampletask?second=two']
        self.command.recipe = recipe

        self.assertRaises(OnlyOneTaskInARowError, self.command.gather_tasks)

    def test_run_tasks(self):
        """Should run all the tasks from run_list, but only once."""
        recipe = Recipe()
        recipe.init_loggers()
        recipe.log.task_log.setLevel(logging.CRITICAL)
        recipe.add_task(ExampleTask)
        task = recipe.task_from_url('/exampletask')

        recipe.validate_dependencies()

        self.command.run_list = [task, task]

        self.command.run_tasks()

        self.assertEqual(1, task.made)

    def test_make(self):
        """Should get recipe, gather tasks and run them."""
        recipe = Recipe()
        recipe.init_loggers()
        recipe.log.task_log.setLevel(logging.CRITICAL)
        recipe.add_task(ExampleTask)
        task = recipe.task_from_url('/exampletask')
        recipe.validate_dependencies()

        self.command.args = ['/exampletask']
        self.command.recipe = recipe

        self.add_mock_object(self.command, 'get_recipe', return_value=recipe)
        self.command.make()

        self.assertEqual(1, task.made)

    def test_make_on_command_abort(self):
        """Should break running tasks on CommandAborted raised."""
        task1 = MagicMock()
        task1.was_runned.return_value = False
        task1.run.side_effect = CommandAborted()

        task2 = MagicMock()
        task2.was_runned.return_value = False

        self.command.run_list = [task1, task2]

        recipe = MagicMock()
        self.add_mock_object(self.command, 'get_recipe', return_value=recipe)
        self.add_mock_object(self.command, 'gather_tasks')

        self.command.make()

        task1.run.assert_called_once_with()
        self.assertEqual(0, task2.run.call_count)
        recipe.log.warning.assert_called_once_with('>> Command aborted!')
