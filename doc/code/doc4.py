from baelfire.core import Core
from baelfire.dependencies import AlwaysTrue
from baelfire.dependencies import TaskRebuilded
from baelfire.task import Task


class MyCore(Core):

    def phase_settings(self):
        super(MyCore, self).phase_settings()
        self.settings['first'] = 'my %(parent)s'
        self.settings['parent'] = 'me'
        self.paths.set('first', 'first.txt', parent='base')


class FirstTask(Task):

    def create_dependecies(self):
        self.build_if(AlwaysTrue())

    def build(self):
        print('S', self.settings['first'])
        self.paths.set('base', 'base', is_root=True)
        print('S', self.paths.get('first'))


class ParentTask(Task):

    def create_dependecies(self):
        self.build_if(TaskRebuilded(FirstTask()))

    def build(self):
        self.settings['parent'] = 'parent'
        print('P', self.settings['first'])
        print('P', self.paths.get('first'))

if __name__ == '__main__':
    ParentTask(MyCore()).run()
