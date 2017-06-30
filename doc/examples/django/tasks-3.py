from baelfire.task import FileTask
from baelfire.task import SubprocessTask
from baelfire.dependencies import FileChanged


class UpdateRequirements(SubprocessTask, FileTask):

    output_name = 'flags:requirements'

    def create_dependecies(self):
        self.build_if(FileChanged('setuppy'))

    def build(self):
        self.popen('{python} {setuppy} develop'.format(
            python=self.paths.get('exe:python'),
            setuppy=self.paths.get('setuppy')),
        )

        open(self.output, 'w').close()
