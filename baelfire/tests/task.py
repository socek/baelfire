import os
from mock import MagicMock

from soktest import TestCase

from baelfire.task import Task
from .recipe import ExampleRecipe
from baelfire.error import CommandAborted
from baelfire.dependencys import Dependency

PREFIX = 'baelfire.task.'


class ExampleDependency(Dependency):

    def __init__(self, return_value):
        super().__init__()
        self.return_value = return_value

    def make(self):
        return self.return_value


class ExampleTask(Task):

    def __init__(self):
        super().__init__()
        self.made = False
        self.dep_1 = ExampleDependency(False)
        self.dep_2 = ExampleDependency(False)
        self.dep_3 = ExampleDependency(False)

    def get_dependencys(self):
        return [self.dep_1, self.dep_2, self.dep_3]

    def generate_dependencys(self):
        self.add_dependecy(self.dep_1)
        self.add_dependecy(self.dep_2)
        self.add_dependecy(self.dep_3)

    def make(self):
        self.made = True

    def get_output_file(self):
        return '/tmp'


class TaskTest(TestCase):

    def setUp(self):
        super().setUp()
        self.task = ExampleTask()

    def test_assign_recipe(self):
        """Should set recipe to a task"""
        recipe = ExampleRecipe()
        self.task.assign_recipe(recipe)

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
        recipe._paths = 'paths'
        self.task.assign_recipe(recipe)

        self.assertEqual('paths', self.task.paths)

    def test_settings(self):
        """Should return settings object from recipe"""
        recipe = ExampleRecipe()
        recipe._settings = 'settings'
        self.task.assign_recipe(recipe)

        self.assertEqual('settings', self.task.settings)

    def test_is_rebuild_needed_false(self):
        """Should return false, if no dependency returned false."""
        recipe = ExampleRecipe()
        self.task.assign_recipe(recipe)

        self.assertEqual(False, self.task.is_rebuild_needed())

    def test_is_rebuild_needed_true(self):
        """Should return false, if one or more dependency returned true."""
        self.task.dep_2.return_value = True
        recipe = ExampleRecipe()
        self.task.assign_recipe(recipe)
        self.task.generate_dependencys()

        self.assertEqual(True, self.task.is_rebuild_needed())

    def test_run_error(self):
        """Should raise error, when no make method specyfied."""
        task = Task()
        self.add_mock_object(task, 'is_rebuild_needed', return_value=True)
        self.assertRaises(AttributeError, task.run)

    def test_run_true(self):
        """Should run make when rebuild is needed."""
        self.add_mock_object(self.task, 'is_rebuild_needed', return_value=True)
        self.task.recipe = MagicMock()
        self.task.dependencys = []
        self.task.run()

        self.assertEqual(True, self.task.made)

    def test_run_false(self):
        """Should not run make when rebuild is not needed."""
        self.add_mock_object(self.task,
                             'is_rebuild_needed',
                             return_value=False)
        self.add_mock_object(self.task, 'logme')
        self.task.run()

        self.assertEqual(False, self.task.made)

    def test_run_force(self):
        """Should run make when force is true."""
        self.add_mock_object(self.task,
                             'is_rebuild_needed',
                             return_value=False)
        self.task.assign_kwargs(force=True)
        self.add_mock_object(self.task, 'logme')
        self.task.recipe = MagicMock()
        self.task.run()

        self.assertEqual(True, self.task.made)

    def test_get_output_file(self):
        """Should return file path"""
        self.assertEqual('/tmp', self.task.get_output_file())

    def test_log(self):
        """Should return log from recipe"""
        recipe = ExampleRecipe()
        recipe.log = 'log'
        self.task.assign_recipe(recipe)

        self.assertEqual('log', self.task.log)

    def test_command(self):
        """Should initialize Process with itself and transport args."""
        self.add_mock(PREFIX + 'Process')
        self.task.command('arg', kw='arg')

        self.mocks['Process'].assert_called_once_with(self.task)
        self.mocks['Process'].return_value.assert_called_once_with(
            'arg', kw='arg')

    def test_touch_when_file_not_exists(self):
        """Should create file if not exists."""
        path = '/tmp/mytestfile.txt'
        self.task.touch(path)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)

    def test_touch_when_file_exists(self):
        """Should update files utime if exists."""
        self.add_mock(PREFIX + 'utime')
        path = '/tmp/mytestfile2.txt'
        fp = open(path, 'w')
        fp.write('test')
        fp.close()

        self.task.touch(path)

        fp = open(path, 'r')
        self.assertEqual('test', fp.read())
        fp.close()
        self.mocks['utime'].assert_called_once_with(path, None)

    def test_add_link(self):
        """Should add task to .links with assigned kwargs."""
        link = ExampleTask()
        recipe = MagicMock()
        recipe.get_task.return_value = link
        self.task.assign_recipe(recipe)

        self.task.add_link('mypath', myarg=10)

        recipe.get_task.assert_called_once_with('mypath')
        self.assertEqual([link], self.task.links)
        self.assertEqual({'myarg': 10}, link.kwargs)

    def test_run_links(self):
        """Should run all links assigned to a task."""
        link = MagicMock()
        recipe = MagicMock()
        recipe.get_task.return_value = link
        self.task.assign_recipe(recipe)
        self.task.add_link('mypath')

        self.task.run_links()

        link.run.assert_called_once_with()

    def test_logme(self):
        """Should log data to a recipe logger."""
        link = MagicMock()
        recipe = MagicMock()
        recipe.get_task.return_value = link
        self.task.assign_recipe(recipe)
        self.task.add_link('mypath')

        self.task.logme('force', 'needed', 'success')

        recipe.data_log.add_task.assert_called_once_with(self.task, {
            'force': 'force',
            'needed': 'needed',
            'success': 'success',
            'links': [link.get_path.return_value],
        })
