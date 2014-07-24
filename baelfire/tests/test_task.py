import os
from mock import MagicMock, create_autospec

from soktest import TestCase

from .test_recipe import ExampleRecipe
from baelfire.dependencies import Dependency
from baelfire.recipe import Recipe
from baelfire.task import Task

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

    def get_dependencies(self):
        return [self.dep_1, self.dep_2, self.dep_3]

    def generate_dependencies(self):
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
        task.recipe = create_autospec(Recipe())
        task.recipe.get_prefix.return_value = '/prefix'

        self.assertEqual('/prefix/sometask', task.get_path())

    def test_get_path_without_path(self):
        """Should return generated path from class name when self.path is
        None"""
        task = ExampleTask()
        task.recipe = create_autospec(Recipe())
        task.recipe.get_prefix.return_value = ''

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
        self.task.generate_dependencies()

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
        self.task.dependencies = []
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
        recipe._log = 'log'
        self.task.assign_recipe(recipe)

        self.assertEqual('log', self.task.log)

    def test_log_with_parent(self):
        """Should return log from parent recipe if avalible"""
        recipe = ExampleRecipe()
        recipe._log = 'log'
        recipe.parent = MagicMock()
        self.task.assign_recipe(recipe)

        self.assertEqual(recipe.parent.log, self.task.log)

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
        recipe.task.return_value = link
        self.task.assign_recipe(recipe)

        self.task.add_link('mypath', myarg=10)

        recipe.task.assert_called_once_with('mypath', myarg=10)
        self.assertEqual([link], self.task.links)

    def test_run_links(self):
        """Should run all links assigned to a task."""
        link = MagicMock()
        recipe = MagicMock()
        recipe.task.return_value = link
        self.task.assign_recipe(recipe)
        self.task.add_link('mypath')

        self.task.run_links()

        link.run.assert_called_once_with()

    def test_logme(self):
        """Should log data to a recipe logger."""
        link = MagicMock()
        recipe = MagicMock()
        recipe.task.return_value = link
        self.task.assign_recipe(recipe)
        self.task.add_link('mypath')
        self.task._log = {
            'force': 'force',
            'needed': 'needed',
            'success': 'success',
            'invoked': [],
        }

        self.task.logme()

        recipe.data_log.add_task.assert_called_once_with(self.task, {
            'force': 'force',
            'needed': 'needed',
            'success': 'success',
            'links': [link.get_path_dotted.return_value],
            'invoked': [],
        })

    def test_run_when_task_was_runned_before(self):
        """Should do nothing if task was runned earlier."""
        self.task.runned = True
        self.add_mock_object(self.task, '_make')

        self.task.run()

        self.assertEqual(0, self.mocks['_make'].call_count)

    def test_invoke_task(self):
        """Should run specyfic task with kwargs assign."""
        self.task.recipe = MagicMock()
        self.task._log = {'invoked': []}

        self.task.invoke_task('/somewhere', data=10)

        task = self.task.recipe.task.return_value

        self.task.recipe.task.assert_called_once_with('/somewhere', data=10)
        task.run.assert_called_once_with()
        self.assertEqual(
            {'invoked': [task.get_path_dotted.return_value]}, self.task._log)

    def test_touchme(self):
        """Should touch file returned by get_output_file."""
        self.add_mock_object(self.task, 'touch')

        self.task.touchme()

        self.mocks['touch'].assert_called_once_with('/tmp')

    def test_is_output_file_avalible_to_build_when_outputfile_not_set(self):
        """Should return False when output file is not set."""
        self.add_mock_object(self.task, 'get_output_file', return_value=None)

        self.assertEqual(False, self.task.is_output_file_avalible_to_build())

    def test_is_output_file_avalible_to_build(self):
        """Should return true when output file is and file is not existing."""
        self.add_mock_object(
            self.task, 'get_output_file', return_value='something')
        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.return_value = False

        self.assertEqual(True, self.task.is_output_file_avalible_to_build())

    def test_ask_for_on_kwargs(self):
        """.ask_for should return data from kwargs"""
        self.task.kwargs['test'] = ['something']

        result = self.task.ask_for('test', 'mylabel')

        self.assertEqual('something', result)

    def test_ask_for(self):
        """.ask_for should ask for value from stdin when value not present in
        kwargs."""
        self.add_mock('builtins.input')

        result = self.task.ask_for('test', 'mylabel')

        self.assertEqual(self.mocks['input'].return_value, result)
        self.mocks['input'].assert_called_once_with('mylabel: ')

    def test_ask_for_setting(self):
        """.ask_for_setting should ask_for value and put it in the settings."""
        settings = {}
        recipe = ExampleRecipe()
        recipe._settings = settings
        self.task.assign_recipe(recipe)
        self.add_mock('builtins.input')

        self.task.ask_for_setting('test', 'mylabel')

        self.assertEqual(self.mocks['input'].return_value, settings['test'])
        self.mocks['input'].assert_called_once_with('mylabel: ')
