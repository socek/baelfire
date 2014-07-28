import inspect
import os
from urllib.parse import urlparse, parse_qs

from smallsettings import Settings, Paths

from .error import TaskNotFoundError
from .log import TaskLogger, Logger
from .signals import SignalHandling
from baelfire import VERSION


class Recipe(object):

    AVAILABLE_TASK_OPTIONS = ['hide']
    prefix = ''

    def __init__(self, is_parent=True):
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
        self._log = None

        self.init_paths()
        self.create_settings()
        self.gather_recipes()
        self.gather_tasks()
        self.init_signals()

        self.final_settings()
        self.final()

        if is_parent:
            self.validate_dependencies()

    @property
    def log(self):
        if self.parent is None:
            return self._log
        else:
            return self.parent.log

    def init_loggers(self):
        """
        Inits logger for running tasks. Should be run on the main recipe and
        only once per proccess.
        """
        self._log = Logger()

    def init_settings(self, settings, paths):
        """
        Inits .settings and .paths.

        :param settings: dict with default settings
        :param paths: dict with default paths
        """
        self._settings = Settings(settings)
        self._paths = Paths(paths)
        self.recipe_paths = Paths()

    def add_recipe(self, recipe):
        """
        Adds child recipe.

        :param recipe: baelfire.recipe.Recipe instance
        """
        recipe.assign_parent(self)
        self.recipes.append(recipe)

    def assign_parent(self, recipe):
        """
        Assign parent recipe.

        :param recipe: baelfire.recipe.Recipe instance
        """
        self.parent = recipe
        recipe._settings.update(self._settings)
        recipe._paths.update(self._paths)
        recipe._tasks.update(self._tasks)
        recipe._tasks_dotted.update(self._tasks_dotted)
        self.data_log = recipe.data_log

    def add_task(self, task_class):
        """
        Add child task.

        :param task: baelfire.task.Task class
        """
        task = task_class()
        task.assign_recipe(self)
        self.tasks[task.get_path()] = task
        self.tasks_dotted[task.get_path_dotted()] = task

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
        try:
            return self.tasks[path]
        except KeyError:
            if self.parent is None:
                return self.tasks[self.prefix + path]
            else:
                raise

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

    def set_path(self, name, dirname, basename, destination='paths'):
        """
        Sets paths.

        :param name: name of the path in .paths
        :param dirname: name of parent path. None == no parent
        :param basename: name of the dir or file. Can be list of folder names,
            whcih will be joined to make a path.
        """
        if type(basename) not in (list, tuple):
            basename = [basename]

        paths = getattr(self, destination)
        if dirname is None:
            paths[name] = basename
        else:
            paths[name] = ['%%(%s)s' % (dirname,)] + basename

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
            if key not in self.AVAILABLE_TASK_OPTIONS:
                raise RuntimeError('Option "%s" is not available!' % (key,))

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

    def init_paths(self):
        """
        Sets initial paths like "pwd" or "recipe_path"
        """
        self.set_path('cwd', None, os.getcwd())
        self.set_path(
            'recipe',
            None,
            os.path.dirname(inspect.getfile(self.__class__)),
            'recipe_paths')
        self.set_path('templates', 'recipe', 'templates', 'recipe_paths')

    def get_prefix(self):
        """
        Return prefix from recipe. This method is for inheritance reasons.
        """
        return self.prefix

    def _filter_task(self, task):
        """
        Filter tasks for printing in list command.
        """
        return True
