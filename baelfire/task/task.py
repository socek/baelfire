from logging import getLogger
from morfdict import PathDict
from morfdict import StringDict

from baelfire.parrented import parrented


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
    def report(self):
        return self._report

    @property
    def myreport(self):
        if self.name not in self.report:
            self.report[self.name] = {}
        return self.report[self.name]

    @property
    def logger(self):
        return getLogger(self.name)

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
        self.phase_dependencies_build()
        self.phase_build()

    def phase_init(self):
        self._settings = StringDict()
        self._paths = PathDict()
        self._report = {'last_index': 0}

        self.myreport['runned'] = False
        self.myreport['needtorun'] = False
        self.myreport['success'] = False
        self.myreport['dependencies'] = {}
        self.myreport['dependencies_run'] = []

        for dependency in self._dependencies:
            self.myreport['dependencies_run'].append(dependency.name)
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
            self.myreport['needtorun'] |= result
        self.logger.debug('Need to run: %s', self.myreport['needtorun'])
        return self.myreport['needtorun']

    def phase_dependencies_build(self):
        for dependency in self._dependencies:
            dependency.phase_build()

    def phase_build(self):
        if self.myreport['needtorun'] and not self.myreport['runned']:
            self.logger.info('Running')
            self.myreport['runned'] = True
            try:
                self.build()
                self.myreport['success'] = True
            except Exception as error:
                self.logger.error(str(error))
                raise

    def add_dependency(self, dependency):
        self._dependencies.append(dependency)
        dependency.set_parent(self)

    def set_parent(self, parent):
        self.parent = parent

    def get_index(self):
        index = self.report['last_index']
        self.report['last_index'] = index + 1
        return index
