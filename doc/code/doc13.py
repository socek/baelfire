from baelfire.core import Core
from baelfire.dependencies import AlwaysTrue
from baelfire.dependencies import TaskRebuilded
from baelfire.task import Task


class MyCore(Core):

    def make_task_inheritance(self):
        super(MyCore, self).make_task_inheritance()
        self.add_task_inheritance(TaskB, TaskD, self._migration)

    def _migration(self, left, right):
        print(left, right)
        return right()


class TaskA(Task):

    def create_dependecies(self):
        self.build_if(AlwaysTrue())

    def build(self):
        print('I am task A')


class TaskB(Task):

    def create_dependecies(self):
        self.build_if(TaskRebuilded(TaskA()))

    def build(self):
        print('I am task B')


class TaskC(Task):

    def create_dependecies(self):
        self.build_if(TaskRebuilded(TaskB()))

    def build(self):
        print('I am task C')


class TaskD(Task):

    def create_dependecies(self):
        self.build_if(TaskRebuilded(TaskA()))

    def build(self):
        print('I am task D')


if __name__ == '__main__':
    TaskC().run()
    print('-------------')
    TaskC(MyCore()).run()
