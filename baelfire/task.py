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

    def logme(self, force, needed, success):
        logdata = {
            'force': force,
            'needed': needed,
            'success': success,
        }
        self.recipe.data_log.add_task(self, logdata)
        for dependency in self.dependencys:
            dependency.logme()

    def run(self):
        try:
            print('\t', self.get_path(), 'S')
            self.pre_run()
            force = self.kwargs.pop('force', False)
            success = None
            needed = self.is_rebuild_needed()

            if needed or force:
                success = False
                self.log.task(self.name)
                self.make(**self.kwargs)
                success = True
        finally:
            self.logme(force, needed, success)
            print('\t', self.get_path(), 'F')

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
