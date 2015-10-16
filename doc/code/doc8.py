from baelfire.dependencies import AlwaysRebuild
from baelfire.task import SubprocessTask


class SimpleProccess(SubprocessTask):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        self.popen(['echo "something"'])


SimpleProccess().run()
