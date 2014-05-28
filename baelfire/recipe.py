from urllib.parse import urlparse, parse_qs

from smallsettings import Settings, Paths

from baelfire import VERSION
from .error import TaskNotFoundError
from .log import TaskLogger, Logger
from .signals import SignalHandling


class Recipe(object):

    AVALIBLE_TASK_OPTIONS = ['hide']

    def __init__(self):
        self.recipes = []
        self._tasks = {}
        self._tasks_dotted = {}
        self.parent = None
        self._spp = None
        self.aborting = False
        self.data_log = TaskLogger()
        self.init_settings({'minimal version': VERSION}, {})
        self.log = None

        self.create_settings()
        self.gather_recipes()
        self.gather_tasks()
        self.validate_dependencies()
        self.init_signals()

        self.final_settings()
        self.final()

    def init_loggers(self):
        self.log = Logger()

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
        self.tasks_dotted[task.get_path_dotted()] = task
        task.assign_recipe(self)

    def task(self, path, method=None, **kwargs):
        for key, value in kwargs.items():
            if not type(value) in [list, tuple]:
                kwargs[key] = [value]

        method = self._dot_searcher if method is None else method

        try:
            task = method(path)
            task.assign_kwargs(**kwargs)
            return task
        except KeyError:
            raise TaskNotFoundError(path)

    def _dot_searcher(self, path):
        path = path if type(path) is str else path.get_path_dotted()
        return self.tasks_dotted[path]

    def _path_searcher(self, path):
        return self.tasks[path]

    def task_from_url(self, url):
        url = urlparse(url)
        path = url.path
        kwargs = parse_qs(url.query)
        task = self.task(path, method=self._path_searcher, **kwargs)
        return task

    def validate_dependencies(self):
        for task in self.tasks.values():
            task.generate_links()
            task.generate_dependencies()

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
    def tasks_dotted(self):
        if self.parent is None:
            return self._tasks_dotted
        else:
            return self.parent.tasks_dotted

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

    def set_task_options(self, path, options={}):
        task = self.task(path)
        for key, value in options.items():
            if key not in self.AVALIBLE_TASK_OPTIONS:
                raise RuntimeError('Option "%s" is not avalible!' % (key,))

            setattr(task, key, value)

    def final_settings(self):
        pass

    def final(self):
        pass
