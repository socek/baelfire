from mock import MagicMock
from soktest import TestCase

from baelfire.error import TaskNotFoundError
from baelfire.recipe import Recipe
from baelfire.task import Task
from baelfire import VERSION


class ExampleTask(Task):

    def generate_dependencies(self):
        pass


class ExampleRecipe(Recipe):

    def create_settings(self):
        self.chronology = ['create_settings']

    def gather_recipes(self):
        self.chronology.append('gather_recipes')

    def gather_tasks(self):
        self.chronology.append('gather_tasks')


class RecipeTest(TestCase):

    def setUp(self):
        super().setUp()
        self.recipe = ExampleRecipe()

    def test_init(self):
        """Should init recipe and run methods in proper order."""
        self.assertEqual(
            [
                'create_settings',
                'gather_tasks',
            ],
            self.recipe.chronology,
        )
        self.assertEqual(VERSION, self.recipe.settings['minimal version'])

    def test_validate_dependencies(self):
        """Should do nothing (test for code coverage)."""
        self.recipe.add_task(Task)
        self.assertEqual(None, self.recipe.validate_dependencies())

    def test_add_task(self):
        """Should instance Task class, set tasks it's parent to self, and add
        this task to self.tasks."""
        self.recipe.add_task(ExampleTask)
        task = self.recipe.task_from_url('/exampletask')

        self.assertEqual(self.recipe, task.recipe)
        self.assertEqual({'/exampletask': task}, self.recipe.tasks)
        self.assertEqual(
            {'baelfire.tests.test_recipe:ExampleTask': task},
            self.recipe.tasks_dotted)

    def test_task_from_url(self):
        """Should return task with assigned kwargs from url."""
        self.recipe.add_task(ExampleTask)

        task = self.recipe.task_from_url(
            '/exampletask?arg=something&arg=somethin2&second_arg=metoo')

        self.assertTrue(isinstance(task, ExampleTask))
        self.assertEqual({
            'arg': ['something', 'somethin2'],
            'second_arg': ['metoo'],
        }, task.kwargs)

    def test_task_bad_name(self):
        """Should raise TaskNotFoundError when task is not found."""
        self.assertRaises(
            TaskNotFoundError,
            self.recipe.task,
            '/exampletask?arg=something&arg=somethin2&second_arg=metoo',
        )

    def test_kwargs(self):
        """Should transform all kwargs arguments into lists."""
        self.recipe.add_task(ExampleTask)
        task = self.recipe.task_from_url('/exampletask')

        task = self.recipe.task(
            'baelfire.tests.test_recipe:ExampleTask',
            one=(1,),
            two=[2, ],
            three=3)

        self.assertEqual((1,), task.kwargs['one'])
        self.assertEqual([2, ], task.kwargs['two'])
        self.assertEqual([3, ], task.kwargs['three'])

    def test_set_task_options_fail(self):
        """set_task_options should raise RuntimeError when invalid option is
        specyfied."""
        self.recipe.add_task(ExampleTask)

        self.assertRaises(
            RuntimeError,
            self.recipe.set_task_options,
            'baelfire.tests.test_recipe:ExampleTask',
            {'elo': 'somethin2'})

    def test_set_task_options(self):
        """set_task_options should set an option to a task"""
        self.recipe.add_task(ExampleTask)

        self.recipe.set_task_options(
            'baelfire.tests.test_recipe:ExampleTask', {'hide': 'somethin2'})
        task = self.recipe.task_from_url('/exampletask')

        self.assertEqual('somethin2', task.hide)

    def test_set_path_when_basename_is_string(self):
        """set_path should set paths with parent name and child joined."""
        self.recipe.paths['parent'] = '/parent'
        self.recipe.set_path('myname', 'parent', 'child')

        self.assertEqual('/parent/child', self.recipe.paths['myname'])

    def test_set_path_when_basename_is_list(self):
        """set_path should set paths with parent name and childs joined."""
        self.recipe.paths['parent'] = '/parent'
        self.recipe.set_path('myname', 'parent', ['first', 'child'])

        self.assertEqual('/parent/first/child', self.recipe.paths['myname'])

    def test_set_path_when_parent_is_none(self):
        """set_path should set child as root path"""
        self.recipe.set_path('myname', None, ['root', 'child'])

        self.assertEqual('root/child', self.recipe.paths['myname'])

    def test_filter_task(self):
        """._filter_task should return True always. It means, print all tasks.
        """
        self.assertEqual(True, self.recipe._filter_task(None))

    def test_get_task_by_url_normal(self):
        """._get_task_by_url should return task when full url is provided"""
        task = MagicMock()
        self.recipe._tasks['/prefix/task'] = task
        self.assertEqual(task, self.recipe._get_task_by_url('/prefix/task'))

    def test_get_task_by_url_no_task_found_with_no_parent(self):
        """._get_task_by_url should raise KeyError when url is not found and no
        parent is present"""
        task = MagicMock()
        self.recipe._tasks['/prefix/task'] = task
        self.assertRaises(
            KeyError, self.recipe._get_task_by_url, '/prefix/task2')

    def test_get_task_by_url_when_provided_without_prefix(self):
        """._get_task_by_url should return task when url without prefix is
        provided"""
        task = MagicMock()
        self.recipe.prefix = '/prefix'
        self.recipe._tasks['/prefix/task'] = task
        self.assertEqual(task, self.recipe._get_task_by_url('/task'))
