from soktest import TestCase

from baelfire.recipe import Recipe
from baelfire.task import Task
from baelfire import VERSION


class ExampleRecipe(Recipe):

    def create_settings(self):
        self.chronology = ['create_settings']

    def post_action(self):
        self.chronology.append('post_action')

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
                          'post_action',
                          'gather_tasks',
                          ],
                         self.recipe.chronology)
        self.assertEqual(VERSION, self.recipe.settings['minimal version'])
        self.assertEqual([], self.recipe.recipes)
        self.assertEqual(None, self.recipe.parent)

    def test_add_recipe(self):
        """Should set recipe it's parent to self, and add this recipe to
        self.recipes."""
        recipe = Recipe()
        self.recipe.add_recipe(recipe)

        self.assertEqual(self.recipe, recipe.parent)
        self.assertEqual([recipe], self.recipe.recipes)

    def test_set_parent(self):
        """Should assign parent to a recipe and update settings and paths."""
        recipe = Recipe()
        recipe.settings['something'] = 'child settings'
        recipe.paths['something'] = 'child paths'
        self.recipe.settings['something'] = 'parent settings'
        self.recipe.paths['something'] = 'parent paths'

        self.recipe.set_parent(recipe)

        print (self.recipe.paths, recipe.paths)
        self.assertEqual(recipe, self.recipe.parent)
        self.assertEqual('child settings', self.recipe.settings['something'])
        self.assertEqual('child paths', self.recipe.paths['something'])
        self.assertEqual(id(recipe.settings), id(self.recipe.settings))
        self.assertEqual(id(recipe.paths), id(self.recipe.paths))

    def test_add_task(self):
        """Should set tasks it's parent to self, and add this task to
        self.tasks."""
        task = Task()
        self.recipe.add_task(task)

        self.assertEqual(self.recipe, task.recipe)
        self.assertEqual([task], self.recipe.tasks)
