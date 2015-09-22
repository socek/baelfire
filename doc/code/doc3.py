import logging

from baelfire.dependencies import FileDoesNotExists
from baelfire.dependencies import RunBefore
from baelfire.dependencies import TaskDependency
from baelfire.task import Task


class FirstTask(Task):

    def create_dependecies(self):
        self.add_dependency(FileDoesNotExists(raw_path='/tmp/me'))

    def build(self):
        with open('/tmp/me', 'w') as myfile:
            myfile.write('something\n')


class SecondTask(Task):

    def create_dependecies(self):
        self.add_dependency(FileDoesNotExists(raw_path='/tmp/me_too'))

    def build(self):
        with open('/tmp/me_too', 'w') as myfile:
            myfile.write('something 2\n')


class ParentTask(Task):

    def create_dependecies(self):
        self.add_dependency(TaskDependency(FirstTask()))
        self.add_dependency(RunBefore(SecondTask()))

    def build(self):
        pass


FORMAT = ' * %(levelname)s %(name)s: %(message)s *'
logging.basicConfig(level=logging.INFO, format=FORMAT)

ParentTask().run()
