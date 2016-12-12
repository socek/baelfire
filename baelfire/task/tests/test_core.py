from baelfire.core import Core
from baelfire.dependencies import AlwaysRebuild
from baelfire.dependencies import RunBefore
from baelfire.task import Task


class ExampleTask(Task):

    def phase_settings(self):
        super(ExampleTask, self).phase_settings()
        self.settings['two'] = '-%(one)s-'
        self.settings['four'] = '+%(three)s+'

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        pass


class ExampleSecondTask(Task):

    def phase_settings(self):
        super(ExampleSecondTask, self).phase_settings()
        self.settings['one'] = 'one222'
        self.settings['five'] = '=%(six)s='

    def create_dependecies(self):
        self.add_dependency(RunBefore(ExampleTask()))
        self.add_dependency(AlwaysRebuild())

    def build(self):
        pass


class MyCore(Core):

    def before_dependencies(self):
        self.settings['one'] = 'one1'
        self.settings['three'] = 'three1'

    def after_dependencies(self):
        self.settings['three'] = 'three3'
        self.settings['six'] = 'six6'


class TestCore(object):

    def test_simple_task(self):
        core = MyCore()
        task = ExampleTask(core)
        task.run()

        assert task.settings['two'] == '-one1-'
        assert task.settings['four'] == '+three3+'

    def test_deep_task(self):
        core = MyCore()
        task = ExampleSecondTask(core)
        task.run()

        assert task.settings['two'] == '-one222-'
        assert task.settings['four'] == '+three3+'
        assert task.settings['five'] == '=six6='
