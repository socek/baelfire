from os import utime, path

from .process import Process


class Task(object):

    recipe = None
    path = None
    dependencies = None
    hide = False
    help = ''

    def __init__(self):
        self.kwargs = {}
        self.links = []
        self.runned = False

    def assign_kwargs(self, **kwargs):
        """
        Assign command line keyword args to this task.

        :param {kwargs}: parameters to assign
        """
        self.kwargs.update(kwargs)

    def assign_recipe(self, recipe):
        """
        Assign recipe to this task.

        :param recipe: baelfire.recipe.Recipe instance
        """
        self.recipe = recipe
        self.dependencies = []

    def add_dependecy(self, dependency):
        """Add dependency to this task.

        :param recipe: baelfire.dependencies.dependency.Dependency instance
        """
        dependency.assign_task(self)
        self.dependencies.append(dependency)

    def get_output_file(self):
        """
        Return output file for this task.
        This method should be overloaded.
        """
        return None

    @property
    def name(self):
        """
        Return name of this task.
        """
        return self.__class__.__name__

    def get_path(self):
        """
        Gets path used in command line.
        """
        if self.path is None:
            return '%s/%s' % (
                self.recipe.get_prefix(),
                self.__class__.__name__.lower())
        else:
            return self.recipe.get_prefix() + self.path

    @classmethod
    def get_path_dotted(cls):
        """
        Gets dotted path of the class.
        """
        module_name = cls.__module__
        recipe_name = cls.__name__
        return '%s:%s' % (module_name, recipe_name)

    def is_rebuild_needed(self):
        """
        Check every dependency and return true if one of them is activated.
        """
        need_rebuild = False

        for dependency in self.dependencies:
            dependency_rule = dependency()
            need_rebuild = need_rebuild or dependency_rule
        need_rebuild = need_rebuild or self.is_output_file_avalible_to_build()

        return need_rebuild

    def is_output_file_avalible_to_build(self):
        """
        Can this task file be builded?
        """
        if self.get_output_file() is None:
            return False
        else:
            return not path.exists(self.get_output_file())

    def pre_run(self):
        """
        Run before checking the dependencies.
        This method should be overloaded.
        """
        pass

    def pre_invoked_tasks(self):
        """
        Run tasks needed to be run before this task.
        This method should be overloaded.
        """
        pass

    def invoke_task(self, path, **kwargs):
        """Run task before this task.

        Keyword arguments:
        :param path: path to a task or baelfire.task.Task instance
        :param {kwargs}: parameters for tasks
        """
        task = self.task(path, **kwargs)
        task.run()
        self._log['invoked'].append(task.get_path_dotted())

    def add_link(self, path, **kwargs):
        """Add linked task.

        :param path: path to a task or baelfire.task.Task instance
        :param [kwargs]: parameters for tasks
        """
        task = self.recipe.task(path, **kwargs)
        self.links.append(task)

    def generate_links(self):
        """
        Method called to generate all linked tasks.
        This method should be overloaded.
        """
        pass

    def run_links(self):
        """
        Run all linked tasks.
        """
        for link in self.links:
            link.run()

    def logme(self):
        """
        Saves log data.
        """
        self._log['links'] = []
        for link in self.links:
            self._log['links'].append(link.get_path_dotted())
        self.recipe.data_log.add_task(self, self._log)
        for dependency in self.dependencies:
            dependency.logme()

    def run(self):
        """
        Run if not runned before.
        """
        if self.runned is False:
            self._log = {}
            try:
                self._before_make()
                if self._log['needed'] or self._log['force']:
                    self._make()
            finally:
                self.logme()
                self.runned = True

    def _before_make(self):
        """
        Prepere for make task.
        """
        self._log['force'] = self.kwargs.pop('force', False)
        self._log['success'] = None
        self._log['needed'] = False
        self._log['output_file'] = self.get_output_file()
        self._log['invoked'] = []

        self.pre_run()
        self.run_links()
        self._log['needed'] = self.is_rebuild_needed()

    def _make(self):
        """
        Make with logging.
        """
        self._log['success'] = False
        self.pre_invoked_tasks()
        self.log.task(self.name)
        self.make()
        self._log['success'] = True

    def was_runned(self):
        """
        Was this task runned?
        """
        return self.name in self.recipe.data_log.tasks

    @property
    def paths(self):
        return self.recipe.paths

    @property
    def recipe_paths(self):
        return self.recipe.recipe_paths

    @property
    def settings(self):
        return self.recipe.settings

    @property
    def log(self):
        return self.recipe.log

    def command(self, *args, **kwargs):
        """
        Run external command.

        :param [args]: args for subproccess.Popen
        :param {kwargs}: keyword args for subproccess.Popen
        """
        process = Process(self)
        return process(*args, **kwargs)

    def touch(self, path):
        """
        Updates file access and modified times specified by path.

        :param path: path to file
        """
        fhandle = open(path, 'a')
        try:
            utime(path, None)
        finally:
            fhandle.close()

    def touchme(self):
        """
        Touch output_file.
        """
        self.touch(self.get_output_file())

    def task(self, path, **kwargs):
        """
        Get task from recipe.

        :param path: path to a task or baelfire.task.Task instance
        :param {kwargs}: parameters for tasks
        """
        return self.recipe.task(path, **kwargs)

    def generate_dependencies(self):
        """
        Method called to generate all dependencies.
        This method should be overloaded.
        """
        pass

    def ask_for(self, key, label):
        """
        Returns value from task args or ask for it from stdin.

        :param key: name of parameter which will be used in task url
        :param label: label used on stdin input
        """
        values = self.kwargs.get(key, [None])
        if values[0] is None:
            return input(label + ': ')
        else:
            print('%s: %s' % (label, values[0]))
            return values[0]

    def ask_for_setting(self, key, label):
        """
        Set setting with value from task args or ask for it from stdin.

        :param key: name of parameter which will be used in task url and in
            settings
        :param label: label used on stdin input
        """
        self.settings[key] = self.ask_for(key, label)
