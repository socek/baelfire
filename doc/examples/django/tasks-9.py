from os import mkdir

from baelfire.dependencies import AlwaysTrue
from baelfire.dependencies import FileChanged
from baelfire.dependencies import FileDoesNotExists
from baelfire.dependencies import PidIsNotRunning
from baelfire.dependencies import TaskRebuilded
from baelfire.task import FileTask
from baelfire.task import SubprocessTask
from baelfire.task import Task
from baelfire.task.screen import AttachScreenTask
from baelfire.task.screen import ScreenTask

from bdjango.dependency import MigrationsChanged


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


class BaseManagePy(SubprocessTask):

    def create_dependecies(self):
        self.run_before(UpdateRequirements())

    def _manage(self, command):
        self.popen(
            '{python} {manage} {command}'.format(
                python=self.paths.get('exe:python'),
                manage=self.paths.get('manage'),
                command=command))


class ApplyMigrations(FileTask, BaseManagePy):
    output_name = 'flags:migrations'

    def create_dependecies(self):
        super(ApplyMigrations, self).create_dependecies()
        self.build_if(FileDoesNotExists(self.output_name))
        self.build_if(MigrationsChanged())
        self.run_before(UpdateRequirements())

    def build(self):
        self._manage('migrate')
        open(self.output, 'w').close()


class StartCelery(ScreenTask):
    screen_name = 'mysite_celery'

    def create_dependecies(self):
        self.run_before(ApplyMigrations())
        self.build_if(PidIsNotRunning(pid_file_name='pid:celery'))

    def build(self):
        self._screen_run(
            ['{celery} -A mysite worker -l info --pidfile={pidfile}'.format(
                celery=self.paths.get('exe:celery'),
                pidfile=self.paths.get('pid:celery'))],
            cwd=self.paths.get('src'))


class AttachCelery(AttachScreenTask):
    detached_task = StartCelery


class StartRunserver(BaseManagePy):

    def create_dependecies(self):
        super(StartRunserver, self).create_dependecies()
        self.run_before(ApplyMigrations())
        self.run_before(StartCelery())
        self.build_if(AlwaysTrue())

    def build(self):
        self._manage('runserver')
