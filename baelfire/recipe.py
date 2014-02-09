from urllib.parse import urlparse, parse_qs

from smallsettings import Settings, Paths

from baelfire import VERSION


class Recipe(object):

    def __init__(self):
        self.recipes = []
        self.tasks = {}
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
        recipe.settings.update(self.settings)
        recipe.paths.update(self.paths)
        recipe.tasks.update(self.tasks)

        self.settings = recipe.settings
        self.paths = recipe.paths
        self.tasks = recipe.tasks

    def add_task(self, task):
        self.tasks[task.get_path()] = task
        task.assign_recipe(self)

    def get_task(self, url):
        url = urlparse(url)
        path = url.path
        kwargs = parse_qs(url.query)

        task = self.tasks[path]
        task.assign_kwargs(**kwargs)
        return task

    def create_settings(self):
        pass

    def gather_recipes(self):
        pass

    def gather_tasks(self):
        pass
