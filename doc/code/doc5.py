import logging

from baelfire.core import Core
from baelfire.dependencies import RunTask
from baelfire.task import FileTask
from baelfire.task import Task


class MyCore(Core):

    def phase_settings(self):
        super().phase_settings()
        self.paths.set('second', '/tmp/second.txt')


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
        self.build_if(RunTask(FirstTask()))
        self.build_if(RunTask(SecondTask()))

    def build(self):
        pass


if __name__ == '__main__':
    FORMAT = ' * %(levelname)s %(name)s: %(message)s *'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    ParentTask(MyCore()).run()
