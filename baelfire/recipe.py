from smallsettings import Settings, Paths

from baelfire import VERSION


class Recipe(object):

    def __init__(self):
        self.settings = Settings({
            'minimal version': VERSION,
        })
        self.paths = Paths()
        self.recipes = []
        self.tasks = []
        self.parent = None

        self.create_settings()
        self.gather_recipes()
        self.post_action()
        self.gather_tasks()

    def add_recipe(self, recipe):
        recipe.set_parent(self)
        self.recipes.append(recipe)

    def set_parent(self, recipe):
        self.parent = recipe

    def add_task(self, task):
        self.tasks.append(task)
        task.set_recipe(self)

    def create_settings(self):
        pass

    def post_action(self):
        pass

    def gather_recipes(self):
        pass

    def gather_tasks(self):
        pass
