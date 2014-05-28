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
        self.assertEqual(['create_settings',
                          'gather_recipes',
                          'gather_tasks',
                          ],
                         self.recipe.chronology)
        self.assertEqual(VERSION, self.recipe.settings['minimal version'])
        self.assertEqual([], self.recipe.recipes)
        self.assertEqual(None, self.recipe.parent)

    def test_validate_dependencies(self):
        """Should do nothing (test for code coverage)."""
        task = Task()
        self.recipe.add_task(task)
        self.assertEqual(None, self.recipe.validate_dependencies())

    def test_add_recipe(self):
        """Should set recipe it's parent to self, and add this recipe to
        self.recipes."""
        recipe = Recipe()
        self.recipe.add_recipe(recipe)

        self.assertEqual(self.recipe, recipe.parent)
        self.assertEqual([recipe], self.recipe.recipes)

    def test_assign_parent(self):
        """Should assign parent to a recipe and update tasks, settings and
        paths."""
        recipe = Recipe()
        recipe.settings['something'] = 'parent settings'
        recipe.paths['something'] = 'parent paths'
        recipe._tasks = {'something 1': 1, 'something': 'parent'}
        self.recipe.settings['something'] = 'child settings'
        self.recipe.paths['something'] = 'child paths'
        self.recipe._tasks = {'something 2': 2, 'something': 'child'}

        self.recipe.assign_parent(recipe)

        self.assertEqual(recipe, self.recipe.parent)
        self.assertEqual('child settings', self.recipe.settings['something'])
        self.assertEqual('child paths', self.recipe.paths['something'])
        self.assertEqual('child settings', recipe.settings['something'])
        self.assertEqual('child paths', recipe.paths['something'])
        self.assertEqual({
            'something 1': 1,
            'something 2': 2,
            'something': 'child',
        }, recipe.tasks)
        self.assertEqual(id(recipe.settings), id(self.recipe.settings))
        self.assertEqual(id(recipe.paths), id(self.recipe.paths))
        self.assertEqual(id(recipe.tasks), id(self.recipe.tasks))
        self.assertEqual(id(recipe.tasks_dotted), id(self.recipe.tasks_dotted))
        self.assertEqual(id(recipe.data_log), id(self.recipe.data_log))

    def test_add_task(self):
        """Should set tasks it's parent to self, and add this task to
        self.tasks."""
        task = ExampleTask()
        self.recipe.add_task(task)

        self.assertEqual(self.recipe, task.recipe)
        self.assertEqual({'/exampletask': task}, self.recipe.tasks)
        self.assertEqual(
            {'baelfire.tests.recipe:ExampleTask': task},
            self.recipe.tasks_dotted)

    def test_task_from_url(self):
        """Should return task with assigned kwargs from url."""
        source_task = ExampleTask()
        self.recipe.add_task(source_task)

        task = self.recipe.task_from_url(
            '/exampletask?arg=something&arg=somethin2&second_arg=metoo')

        self.assertEqual(task, source_task)
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
        self.recipe.add_task(ExampleTask())

        task = self.recipe.task(
            'baelfire.tests.recipe:ExampleTask', one=(1,), two=[2, ], three=3)

        self.assertEqual((1,), task.kwargs['one'])
        self.assertEqual([2, ], task.kwargs['two'])
        self.assertEqual([3, ], task.kwargs['three'])

    def test_set_task_options_fail(self):
        """set_task_options should raise RuntimeError when invalid option is
        specyfied."""
        self.recipe.add_task(ExampleTask())

        self.assertRaises(
            RuntimeError,
            self.recipe.set_task_options,
            'baelfire.tests.recipe:ExampleTask',
            {'elo': 'somethin2'})

    def test_set_task_options(self):
        """set_task_options should set an option to a task"""
        task = ExampleTask()
        self.recipe.add_task(task)

        self.recipe.set_task_options(
            'baelfire.tests.recipe:ExampleTask', {'hide': 'somethin2'})

        self.assertEqual('somethin2', task.hide)
