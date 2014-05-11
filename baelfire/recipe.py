from urllib.parse import urlparse, parse_qs

from smallsettings import Settings, Paths

from baelfire import VERSION
from .error import TaskNotFoundError
from .log import TaskLogger, Logger
from .signals import SignalHandling


class Recipe(object):

    def __init__(self):
        self.recipes = []
        self._tasks = {}
        self.parent = None
        self._spp = None
        self.aborting = False
        self.data_log = TaskLogger()
        self.log = Logger()
        self.init_settings({'minimal version': VERSION}, {})

        self.create_settings()
        self.gather_recipes()
        self.gather_tasks()
        self.validate_dependencys()
        self.init_signals()

    def init_settings(self, settings, paths):
        self._settings = Settings(settings)
        self._paths = Paths(paths)

    def add_recipe(self, recipe):
        recipe.assign_parent(self)
        self.recipes.append(recipe)

    def assign_parent(self, recipe):
        self.parent = recipe
        recipe._settings.update(self._settings)
        recipe._paths.update(self._paths)
        recipe._tasks.update(self._tasks)
        recipe.data_log = self.data_log

    def add_task(self, task):
        self.tasks[task.get_path()] = task
        task.assign_recipe(self)

    def task(self, path, **kwargs):
        for key, value in kwargs.items():
            if not type(value) in [list, tuple]:
                kwargs[key] = [value]
        try:
            task = self.tasks[path]
            task.assign_kwargs(**kwargs)
            return task
        except KeyError:
            raise TaskNotFoundError(path)

    def task_from_url(self, url):
        url = urlparse(url)
        path = url.path
        kwargs = parse_qs(url.query)
        task = self.task(path, **kwargs)
        return task

    def validate_dependencys(self):
        for task in self.tasks.values():
            task.generate_links()
            task.generate_dependencys()

    def init_signals(self):
        self.signal_handling = SignalHandling(self)

    def create_settings(self):
        pass

    def gather_recipes(self):
        pass

    def gather_tasks(self):
        pass

    @property
    def tasks(self):
        if self.parent is None:
            return self._tasks
        else:
            return self.parent.tasks

    @property
    def settings(self):
        if self.parent is None:
            return self._settings
        else:
            return self.parent.settings

    @property
    def paths(self):
        if self.parent is None:
            return self._paths
        else:
            return self.parent.paths
