from os import mkdir

from baelfire.dependencies import FileChanged
from baelfire.dependencies import TaskRebuilded
from baelfire.task import FileTask
from baelfire.task import SubprocessTask


class CreateFlagsFolder(FileTask):

    output_name = 'flags'

    def build(self):
        mkdir(self.output)


class UpdateRequirements(SubprocessTask, FileTask):

    output_name = 'flags:requirements'

    def create_dependecies(self):
        self.build_if(TaskRebuilded(CreateFlagsFolder()))
        self.build_if(FileChanged('setuppy'))

    def build(self):
        self.popen('{python} {setuppy} develop'.format(
            python=self.paths.get('exe:python'),
            setuppy=self.paths.get('setuppy')),
        )

        open(self.output, 'w').close()
