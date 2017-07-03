from os import mkdir

from baelfire.dependencies import AlwaysTrue
from baelfire.dependencies import FileChanged
from baelfire.dependencies import TaskRebuilded
from baelfire.task import FileTask
from baelfire.task import SubprocessTask
from baelfire.task import Task


class CreateFlagsFolder(FileTask):

    output_name = 'flags'

    def build(self):
        mkdir(self.output)


class BaseRequirements(SubprocessTask, FileTask):

    def create_dependecies(self):
        super(BaseRequirements, self).create_dependecies()
        self.build_if(TaskRebuilded(CreateFlagsFolder()))

    def _update_flag(self):
        open(self.output, 'w').close()


class SetupPyDevelop(BaseRequirements):
    output_name = 'flags:setuppy'

    def create_dependecies(self):
        super(SetupPyDevelop, self).create_dependecies()
        self.build_if(FileChanged('setuppy'))

    def build(self):
        self.popen(
            '{python} {setuppy} develop'.format(
                python=self.paths.get('exe:python'),
                setuppy=self.paths.get('setuppy')))

        self._update_flag()


class UpdateRequirementsProduction(BaseRequirements):
    output_name = 'flags:requirements'

    def create_dependecies(self):
        super(UpdateRequirementsProduction, self).create_dependecies()
        self.build_if(FileChanged('requirementst_production'))

    def build(self):
        self.popen(
            '{pip} install -r {file}'.format(
                pip=self.paths.get('exe:pip'),
                file=self.paths.get('requirementst_production')))

        self._update_flag()


class UpdateRequirements(Task):

    def create_dependecies(self):
        self.run_before(SetupPyDevelop())
        self.run_before(UpdateRequirementsProduction())

    def build(self):
        pass


class StartRunserver(SubprocessTask):

    def create_dependecies(self):
        self.run_before(UpdateRequirements())
        self.build_if(AlwaysTrue())

    def build(self):
        self.popen(
            '{python} {manage} runserver'.format(
                python=self.paths.get('exe:python'),
                manage=self.paths.get('manage')))
