from baelfire.dependencies import AlwaysTrue
from baelfire.task import SubprocessTask


class UpdateRequirements(SubprocessTask):

    def create_dependecies(self):
        self.build_if(AlwaysTrue())

    def build(self):
        self.popen('python setup.py develop')
