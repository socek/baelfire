from smallsettings import Settings, Paths

from baelfire import VERSION


class Recipe(object):

    def __init__(self):
        self.settings = Settings({
            'minimal version': VERSION,
        })
        self.paths = Paths()
        self.recipes = []
        self.parent = None

        self.create_settings()
        self.gather_recipes()
        self.post_action()

    def add_recipe(self, recipe):
        recipe.set_parent(self)
        self.recipes.append(recipe)

    def set_parent(self, recipe):
        self.parent = recipe

    def create_settings(self):
        pass

    def post_action(self):
        pass

    def gather_recipes(self):
        pass
