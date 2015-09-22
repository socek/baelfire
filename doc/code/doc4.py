from baelfire.dependencies import AlwaysRebuild
from baelfire.dependencies import TaskDependency
from baelfire.task import Task


class FirstTask(Task):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def phase_settings(self):
        super().phase_settings()
        self.settings['first'] = 'my %(parent)s'
        self.settings['parent'] = 'me'
        self.paths['first'] = ['%(base)s', 'first.txt']

    def build(self):
        print('S', self.settings['first'])
        print('S', self.paths['first'])


class ParentTask(Task):

    def create_dependecies(self):
        self.add_dependency(TaskDependency(FirstTask()))

    def phase_settings(self):
        super().phase_settings()
        self.settings['parent'] = 'parent'
        self.paths['base'] = '/base'

    def build(self):
        print('P', self.settings['first'])
        print('P', self.paths['first'])


ParentTask().run()
