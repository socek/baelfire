import logging

from baelfire.dependencies import RunBefore
from baelfire.task import FileTask
from baelfire.task import Task


class FirstTask(FileTask):
    output = '/tmp/first.txt'

    def build(self):
        with open(self.output, 'w') as myfile:
            myfile.write('First')


class SecondTask(FileTask):
    output_name = 'second'

    def build(self):
        with open(self.output, 'w') as myfile:
            myfile.write('Second')


class ParentTask(Task):

    def create_dependecies(self):
        self.add_dependency(RunBefore(FirstTask()))
        self.add_dependency(RunBefore(SecondTask()))

    def phase_settings(self):
        super().phase_settings()
        self.paths['second'] = '/tmp/second.txt'

    def build(self):
        pass

FORMAT = ' * %(levelname)s %(name)s: %(message)s *'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


ParentTask().run()
