from soktest import TestCase

from baelfire.recipe import Recipe
from baelfire import VERSION


class ExampleRecipe(Recipe):

    def create_settings(self):
        self.chronology = ['create_settings']

    def post_action(self):
        self.chronology.append('post_action')

    def gather_recipes(self):
        self.chronology.append('gather_recipes')


class RecipeTest(TestCase):

    def setUp(self):
        super().setUp()
        self.recipe = ExampleRecipe()

    def test_init(self):
        """Should init recipe and run methods in proper order."""
        self.assertEqual(['create_settings',
                          'gather_recipes',
                          'post_action'],
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
        """Should assign parent to a recipe."""
        self.recipe.set_parent('my parrent')

        self.assertEqual('my parrent', self.recipe.parent)
