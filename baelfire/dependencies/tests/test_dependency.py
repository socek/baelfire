from mock import MagicMock

from soktest import TestCase

from baelfire.recipe import Recipe
from baelfire.tests.test_task import ExampleTask
from ..dependency import Dependency, AlwaysRebuild


class ExampleDependency(Dependency):

    def __init__(self):
        super().__init__()
        self.running = []

    def validate_task(self):
        self.running.append('validate_task')

    def validate_parent(self):
        self.running.append('validate_parent')

    def validate_dependency(self):
        self.running.append('validate_dependency')

    def make(self):
        self.running.append('make')
        return 'make'


class DependencyTest(TestCase):

    def setUp(self):
        super().setUp()
        self.task = ExampleTask()
        self.dependency = ExampleDependency()
        self.dependency.assign_task(self.task)

    def test_init(self):
        dependency = Dependency()

        self.assertEqual(None, dependency.task)
        self.assertEqual(None, dependency.parent)

    def test_assign_task(self):
        """Should assign task"""
        self.assertEqual(self.task, self.dependency.task)

    def test_assign_parent(self):
        """Should assign parent"""
        task = ExampleTask()
        self.dependency.assign_parent(task)
        self.assertEqual(task, self.dependency.parent)

    def test_call(self):
        """Should run validation of task, parent and then run make method."""
        self.assertEqual('make', self.dependency())
        self.assertEqual(
            ['validate_task', 'validate_parent',
                'validate_dependency', 'make'],
            self.dependency.running)

    def test_run_parent(self):
        """Calling dependency should run parent when exists."""
        task = ExampleTask()
        task.recipe = MagicMock()
        task.dependencies = []
        task.generate_dependencies()
        task.kwargs['force'] = True
        self.add_mock_object(task, 'logme')
        self.dependency.assign_parent(task)

        self.dependency()

        self.assertEqual(True, task.made)

    def test_name(self):
        """Should return class name"""
        self.assertEqual('ExampleDependency', self.dependency.name)

    def test_logme(self):
        """Should add dependency to log in the recipe."""
        self.dependency.task = MagicMock()
        self.dependency.task.name = 'taskname'
        self.dependency.task.recipe = Recipe()
        self.dependency.task.recipe.data_log.tasks[
            'taskname'] = {'dependencies': []}
        self.dependency.logdata = {
            'data': 'example data',
        }
        self.dependency.logme()

        self.assertEqual(
            [{'name': 'ExampleDependency', 'data': {'data': 'example data'}}],
            self.dependency.task.recipe.data_log.tasks[
                'taskname']['dependencies'],
        )

    def test_logme_when_dependency_not_runned(self):
        """Should use 'default' log for dependency when it was nor runned."""

        self.dependency.task = MagicMock()
        self.dependency.task.name = 'taskname'
        self.dependency.task.recipe = Recipe()
        self.dependency.task.recipe.data_log.tasks[
            'taskname'] = {'dependencies': []}
        self.dependency.logme()

        self.assertEqual(
            [{'name': 'ExampleDependency', 'data': {'runned': False}}],
            self.dependency.task.recipe.data_log.tasks[
                'taskname']['dependencies'],
        )


class AlwaysRebuildTest(TestCase):

    def test_simple(self):
        """Should always return True."""
        dependency = AlwaysRebuild()
        self.assertEqual(True, dependency())
