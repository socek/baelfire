from baelfire.core import Core
from baelfire.dependencies import AlwaysRebuild
from baelfire.dependencies.task import RunBefore
from baelfire.task import Task


class ExampleTask(Task):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        self.top_core.flags['ExampleTask'] = True


class FakeTask(Task):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        self.top_core.flags['FakeTask'] = True


class ExampleTaskInherited(Task):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        self.top_core.flags['ExampleTaskInherited'] = True


class ExampleTaskInheritedSecond(Task):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        self.top_core.flags['ExampleTaskInheritedSecond'] = True


class RootTask(Task):

    def create_dependecies(self):
        self.add_dependency(RunBefore(ExampleTask()))
        self.add_dependency(RunBefore(FakeTask()))
        self.add_dependency(AlwaysRebuild())

    def build(self):
        if self.parent:
            self.parent.core.flags['RootTask'] = True
        else:
            self.core.flags['RootTask'] = True


class DeepInheritanceTask(Task):

    def create_dependecies(self):
        self.add_dependency(RunBefore(RootTask()))
        self.add_dependency(AlwaysRebuild())

    def build(self):
        self.top_core.flags['DeepInheritanceTask'] = True


class MyCore(Core):

    def __init__(self):
        super(MyCore, self).__init__()
        self.flags = dict()

    def phase_settings(self):
        self.settings['one'] = 'one1'
        self.settings['three'] = 'three1'
        self.settings['two'] = '-%(one)s-'
        self.settings['four'] = '+%(three)s+'


class InheritanceCore(Core):

    def __init__(self):
        super(InheritanceCore, self).__init__()
        self.flags = dict()

    def make_task_inheritance(self):
        self.add_task_inheritance(ExampleTask, ExampleTaskInherited)


class TestCore(object):

    def test_simple_task(self):
        core = MyCore()
        task = ExampleTask(core)
        task.run()

        assert task.settings['two'] == '-one1-'
        assert task.settings['four'] == '+three1+'
        assert core.flags.get('ExampleTask')
        assert not core.flags.get('ExampleTaskInherited')


class TestInheritance(object):

    def test_inheritance_core(self):
        core = InheritanceCore()
        task = RootTask(core)
        task.run()

        assert not core.flags.get('ExampleTask')
        assert core.flags.get('ExampleTaskInherited')
        assert core.flags.get('RootTask')

    def test_no_inheritance_core(self):
        core = MyCore()
        task = RootTask(core)
        task.run()

        assert core.flags.get('ExampleTask')
        assert not core.flags.get('ExampleTaskInherited')
        assert core.flags.get('RootTask')

    def test_deep_inheritance(self):
        core = InheritanceCore()
        task = DeepInheritanceTask(core)
        task.run()

        assert not core.flags.get('ExampleTask')
        assert core.flags.get('ExampleTaskInherited')
        assert core.flags.get('RootTask')
        assert core.flags.get('DeepInheritanceTask')

    def test_double_inheritance(self):
        core = InheritanceCore()
        core.add_task_inheritance(ExampleTask, ExampleTaskInheritedSecond)
        core.add_task_inheritance(FakeTask, ExampleTaskInheritedSecond)
        task = DeepInheritanceTask(core)
        task.run()

        assert not core.flags.get('ExampleTask')
        assert not core.flags.get('ExampleTaskInherited')
        assert core.flags.get('ExampleTaskInheritedSecond')
        assert core.flags.get('RootTask')
        assert core.flags.get('DeepInheritanceTask')
