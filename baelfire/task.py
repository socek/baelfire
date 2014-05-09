from os import utime

from .process import Process


class Task(object):

    recipe = None
    path = None
    dependencys = None
    hide = False
    help = ''

    def __init__(self):
        self.kwargs = {}
        self.links = []
        self.runned = False

    def assign_kwargs(self, **kwargs):
        self.kwargs.update(kwargs)

    def assign_recipe(self, recipe):
        self.recipe = recipe
        self.dependencys = []

    def add_dependecy(self, dependency):
        dependency.assign_task(self)
        self.dependencys.append(dependency)

    def get_output_file(self):
        return None

    @property
    def name(self):
        return self.__class__.__name__

    def get_path(self):
        """get_path(self) -> str
        Returns path (for using in command line) of the tasks provided by class
        value path, or just classname if path == None.
        """
        if self.path is None:
            return '/' + self.__class__.__name__.lower()
        else:
            return self.path

    def is_rebuild_needed(self):
        need_rebuild = False

        for dependency in self.dependencys:
            dependency_rule = dependency()
            need_rebuild = need_rebuild or dependency_rule

        return need_rebuild

    def pre_run(self):
        pass

    def pre_invoked_tasks(self):
        pass

    def invoke_task(self, path, **kwargs):
        task = self.recipe.get_task(path)
        task.assign_kwargs(**kwargs)
        task.run()

    def add_link(self, path, **kwargs):
        task = self.recipe.get_task(path)
        task.assign_kwargs(**kwargs)
        self.links.append(task)

    def generate_links(self):
        pass

    def run_links(self):
        for link in self.links:
            link.run()

    def logme(self):
        self._log['links'] = []
        for link in self.links:
            self._log['links'].append(link.get_path())
        self.recipe.data_log.add_task(self, self._log)
        for dependency in self.dependencys:
            dependency.logme()

    def run(self):
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
        self._log['force'] = self.kwargs.pop('force', False)
        self._log['success'] = None
        self._log['needed'] = False

        self.pre_run()
        self.run_links()
        self._log['needed'] = self.is_rebuild_needed()

    def _make(self):
        self._log['success'] = False
        self.pre_invoked_tasks()
        self.log.task(self.name)
        self.make(**self.kwargs)
        self._log['success'] = True

    def was_runned(self):
        """Was this task runned?"""
        return self.name in self.recipe.data_log.tasks

    @property
    def paths(self):
        return self.recipe.paths

    @property
    def settings(self):
        return self.recipe.settings

    @property
    def log(self):
        return self.recipe.log

    def command(self, *args, **kwargs):
        """Run external command."""
        process = Process(self)
        return process(*args, **kwargs)

    def touch(self, path):
        """touch(filename) -> None
        Updates file access and modified times specified by path.
        """
        fhandle = open(path, 'a')
        try:
            utime(path, None)
        finally:
            fhandle.close()

    def touchme(self):
        self.touch(self.get_output_file())
