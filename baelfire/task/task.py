from logging import getLogger
from yaml import dump

from baelfire.parrented import parrented
from baelfire.core import Core


class Task(object):
    """
    Normal task.
    """

    @property
    def name(self):
        """
        Return name of this task.
        """
        return self.__module__ + "." + self.__class__.__name__

    @property
    @parrented
    def settings(self):
        return self.core.settings

    @property
    @parrented
    def paths(self):
        return self.core.paths

    @property
    @parrented
    def report(self):
        return self.core.report

    @property
    def myreport(self):
        if self.name not in self.report:
            self.report[self.name] = {}
        return self.report[self.name]

    @property
    def logger(self):
        return getLogger(self.name)

    def __init__(self, core=None):
        self._dependencies = []
        self.parent = None

        self._args = {}
        self.core = core or Core()
        self.create_dependecies()

    def run(self):
        """
        Check all dependencies and rebuild if needed.
        """
        self._step_validation()
        self._step_build()

    def _step_validation(self):
        self.phase_init()
        self.phase_settings()
        self.phase_data()
        self.phase_validation()

    def _step_build(self):
        self.phase_dependencies_build()
        self.phase_build()

    def phase_init(self):
        self.core.init()

        self.paths.set('report', '.baelfire.report')

        self.myreport['runned'] = False
        self.myreport['needtorun'] = False
        self.myreport['success'] = False
        self.myreport['dependencies'] = []

        for dependency in self._dependencies:
            self.myreport['dependencies'].append(dependency.myreport)
            dependency.phase_init()

    def phase_settings(self):
        self.core.phase_settings()

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
        """
        Add dependency to a task.
        """
        self._dependencies.append(dependency)
        dependency.set_parent(self)

    def set_parent(self, parent):
        self.parent = parent

    def get_index(self):
        index = self.report['last_index']
        self.report['last_index'] = index + 1
        return index

    def save_report(self):
        """
        Save report file after task run.
        """
        with open(self.paths.get('report'), 'w') as file:
            dump(self.report, file, default_flow_style=False)
        return self.paths.get('report')

    @property
    def top_core(self):
        if self.parent:
            return self.parent.top_core
        else:
            return self.core
