from baelfire.core import Core
from baelfire.dependencies import AlwaysTrue
from baelfire.task import Task


class MyCore(Core):

    def phase_settings(self):
        super(MyCore, self).phase_settings()
        self.settings['something'] = 'hello'


class MyTask(Task):

    def create_dependecies(self):
        self.build_if(AlwaysTrue())

    def build(self):
        print(self.settings['something'])


def run():
    return MyTask(MyCore())
