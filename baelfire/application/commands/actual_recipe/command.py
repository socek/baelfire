from ..command import TriggeredCommand


class ActualRecipe(TriggeredCommand):

    def __init__(self):
        super().__init__('-c',
                         '--actual-recipe',
                         help='Print actual recipe path')

    def make(self):
        self.recipe = self.get_recipe()
        module_name = self.recipe.__class__.__module__
        recipe_name = self.recipe.__class__.__name__
        print('%s:%s' % (module_name, recipe_name))
