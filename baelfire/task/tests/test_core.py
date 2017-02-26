from baelfire.core import Core
from baelfire.dependencies import AlwaysRebuild
from baelfire.task import Task


class ExampleTask(Task):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        pass


class MyCore(Core):

    def phase_settings(self):
        self.settings['one'] = 'one1'
        self.settings['three'] = 'three1'
        self.settings['two'] = '-%(one)s-'
        self.settings['four'] = '+%(three)s+'


class TestCore(object):

    def test_simple_task(self):
        core = MyCore()
        task = ExampleTask(core)
        task.run()

        assert task.settings['two'] == '-one1-'
        assert task.settings['four'] == '+three1+'
