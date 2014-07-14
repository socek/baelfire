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
        self.init_settings(
            {'minimal version': VERSION},
            {})
        self.log = None

        self.create_settings()
        self.gather_recipes()
        self.gather_tasks()
        self.validate_dependencies()
        self.init_signals()

        self.final_settings()
        self.final()

    def init_loggers(self):
        """
        Inits logger for running tasks. Should be run on the main recipe and
        only once per proccess.
        """
        self.log = Logger()

    def init_settings(self, settings, paths):
        """
        Inits .settings and .paths.

        :param settings: dict with default settings
        :param paths: dict with default paths
        """
        self._settings = Settings(settings)
        self._paths = Paths(paths)

    def add_recipe(self, recipe):
        """
        Adds child recipe.

        :param recipe: baelfire.recipe.Recipe instance
        """
        recipe.assign_parent(self)
        self.recipes.append(recipe)
        self._tasks.update(recipe._tasks)
        self._tasks_dotted.update(recipe._tasks_dotted)

    def assign_parent(self, recipe):
        """
        Assign parent recipe.

        :param recipe: baelfire.recipe.Recipe instance
        """
        self.parent = recipe
        recipe._settings.update(self._settings)
        recipe._paths.update(self._paths)
        recipe._tasks.update(self._tasks)
        recipe.data_log = self.data_log

    def add_task(self, task_class):
        """
        Add child task.

        :param task: baelfire.task.Task class
        """
        task = task_class()
        self.tasks[task.get_path()] = task
        self.tasks_dotted[task.get_path_dotted()] = task
        task.assign_recipe(self)

    def task(self, path, method=None, **kwargs):
        """
        Return task assigned to this, parent or child recipes.

        :param path: path to the task
        :param method: method to use which gets the task
        :param {kwargs}: parameters for tasks
        """
        for key, value in kwargs.items():
            if not type(value) in [list, tuple]:
                kwargs[key] = [value]

        method = self._get_task_by_dotted_path if method is None else method

        try:
            task = method(path)
            task.assign_kwargs(**kwargs)
            return task
        except KeyError:
            raise TaskNotFoundError(path)

    def _get_task_by_dotted_path(self, path):
        """
        Get task using Python import path.

        :param path: dotted path to the task
        """
        path = path if type(path) is str else path.get_path_dotted()
        return self.tasks_dotted[path]

    def task_from_url(self, url):
        """
        Get task and assign kwargs from url.

        :param url: path to the task with parameters
        """
        url = urlparse(url)
        path = url.path
        kwargs = parse_qs(url.query)
        task = self.task(path, method=self._get_task_by_url, **kwargs)
        return task

    def _get_task_by_url(self, path):
        """
        Get task by url.

        :param path: path to the task
        """
        return self.tasks[path]

    def validate_dependencies(self):
        """
        Validates links and dependencies for all tasks.
        """
        for task in self.tasks.values():
            task.generate_links()
            task.generate_dependencies()

    def init_signals(self):
        """
        Init catching of system signals.
        """
        self.signal_handling = SignalHandling(self)

    def create_settings(self):
        """
        Place your settings and paths here.
        This method should be overloaded.
        """

    def gather_recipes(self):
        """
        Place your child recipes here.
        This method should be overloaded.
        """

    def gather_tasks(self):
        """
        Place your tasks here.
        This method should be overloaded.
        """

    @property
    def tasks(self):
        """
        All the tasks by url.
        """
        if self.parent is None:
            return self._tasks
        else:
            return self.parent.tasks

    @property
    def tasks_dotted(self):
        """
        All the tasks by dotted path.
        """
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
        """
        Sets options for task.

        :param path: path to the task
        :param options: dict of options
        """
        task = self.task(path)
        for key, value in options.items():
            if key not in self.AVALIBLE_TASK_OPTIONS:
                raise RuntimeError('Option "%s" is not avalible!' % (key,))

            setattr(task, key, value)

    def final_settings(self):
        """
        Place your final settings and paths here. This method is invoked at
        the end of creating recipe. This settings will not be changed by child
        recipes.
        This method should be overloaded.
        """

    def final(self):
        """
        Place your final "something" here. This method is invoked at the end of
        creating recipe.
        This method should be overloaded.
        """
