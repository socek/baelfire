from smallsettings import Settings, Paths

from baelfire import VERSION


class Recipe(object):

    def __init__(self):
        self.recipes = []
        self.tasks = []
        self.parent = None
        self.init_settings({'minimal version': VERSION}, {})

        self.create_settings()
        self.gather_recipes()
        self.gather_tasks()

    def init_settings(self, settings, paths):
        self.settings = Settings(settings)
        self.paths = Paths(paths)

    def add_recipe(self, recipe):
        recipe.assign_parent(self)
        self.recipes.append(recipe)

    def assign_parent(self, recipe):
        self.parent = recipe
        self.settings.update(recipe.settings)
        recipe.settings = self.settings
        recipe.paths = self.paths.update(recipe.paths)
        recipe.paths = self.paths
        recipe.tasks += self.tasks

    def add_task(self, task):
        self.tasks.append(task)
        task.assign_recipe(self)

    def create_settings(self):
        pass

    def gather_recipes(self):
        pass

    def gather_tasks(self):
        pass
