from baelfire.dependencies import AlwaysTrue
from baelfire.task import SubprocessTask


class SimpleProccess(SubprocessTask):

    def create_dependecies(self):
        self.build_if(AlwaysTrue())

    def build(self):
        self.popen('echo "something"')

if __name__ == '__main__':
    SimpleProccess().run()
