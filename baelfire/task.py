from morfdict import PathDict
from morfdict import StringDict

from .parrented import parrented


class Task(object):

    @property
    def name(self):
        """
        Return name of this task.
        """
        return self.__module__ + "." + self.__class__.__name__

    @property
    @parrented
    def settings(self):
        return self._settings

    @property
    @parrented
    def paths(self):
        return self._paths

    @property
    @parrented
    def datalog(self):
        return self._datalog

    @property
    @parrented
    def args(self):
        return self._args

    @property
    def mylog(self):
        if self.name not in self.datalog:
            self.datalog[self.name] = {}
        return self.datalog[self.name]

    @property
    def myargs(self):
        if self.name not in self.args:
            self.args[self.name] = ([], {})
        return self.args[self.name]

    def __init__(self):
        self._dependencies = []
        self.parent = None

        self._args = {}
        self.create_dependecies()

    def run(self):
        self.phase_init()
        self.phase_settings()
        self.phase_data()
        self.phase_validation()
        self.phase_run()
        self.phase_myrun()

    def phase_init(self):
        self._settings = StringDict()
        self._paths = PathDict()
        self._datalog = {'last_index': 0}

        self.mylog['runned'] = False
        self.mylog['needtorun'] = False
        self.mylog['success'] = False
        self.mylog['dependencies'] = {}
        self.mylog['dependencies_run'] = []

        for dependency in self._dependencies:
            self.mylog['dependencies_run'].append(dependency.name)
            dependency.phase_init()

    def phase_settings(self):
        for dependency in self._dependencies:
            dependency.phase_settings()

    def phase_data(self):
        for dependency in self._dependencies:
            dependency.phase_data()

    def phase_validation(self):
        for dependency in self._dependencies:
            result = dependency.phase_validation()
            self.mylog['needtorun'] |= result
        return self.mylog['needtorun']

    def phase_run(self):
        for dependency in self._dependencies:
            dependency.phase_run()

    def phase_myrun(self):
        if self.mylog['needtorun']:
            self.mylog['runned'] = True
            args, kwargs = self.myargs
            self.make(*args, **kwargs)
            self.mylog['success'] = True

    def add_dependency(self, dependency):
        self._dependencies.append(dependency)
        dependency.set_parent(self)

    def set_myargs(self, *args, **kwargs):
        self.set_args(self.name, *args, **kwargs)

    def set_args(self, obj, *args, **kwargs):
        name = self._name_or_cls(obj)
        self.args[name] = (args, kwargs)

    def _name_or_cls(self, obj):
        if type(obj) is str:
            return obj
        else:
            return obj.__module__ + '.' + obj.__name__

    def set_parent(self, parent):
        self.parent = parent

    def get_index(self):
        index = self.datalog['last_index']
        self.datalog['last_index'] = index + 1
        return index

    def make(self):
        pass
