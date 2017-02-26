from pytest import fixture
from pytest import raises
from yaml import load

from baelfire.core import Core
from baelfire.dependencies import AlwaysRebuild
from baelfire.dependencies import TaskDependency
from baelfire.dependencies.dependency import NoRebuild
from baelfire.task import Task


class ExampleCore(Core):

    def phase_settings(self):
        super(ExampleCore, self).phase_settings()
        self.settings['child'] = '2'
        self.paths.set('child', 'child.txt')

        self.settings['parent'] = '1'
        self.paths.set('parent', 'parent.txt')


class ExampleTask(Task):

    def create_dependecies(self):
        pass

    def build(self):
        pass


class ExampleFailingTask(Task):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        raise RuntimeError('failing')


class ExampleChild(ExampleTask):

    def build(self):
        self._data = {
            'settings': {
                'child': self.settings['child'],
                'parent': self.settings['parent']
            },
            'paths': {
                'child': self.paths.get('child'),
                'parent': self.paths.get('parent'),
            },
        }


class ExampleParent(ExampleTask):

    def build(self):
        self._data = {
            'settings': {
                'child': self.settings['child'],
                'parent': self.settings['parent']
            },
            'paths': {
                'child': self.paths.get('child'),
                'parent': self.paths.get('parent'),
            },
        }


class TestTask(object):

    @fixture
    def task(self):
        return ExampleTask()

    def test_simple_flow(self, task):
        """
        Sanity check. This test simple run without dependecies or build.
        """
        task.run()

        assert task.report == {
            'baelfire.task.tests.test_tasks.ExampleTask': {
                'dependencies': [],
                'needtorun': False,
                'runned': False,
                'success': False,
            },
            'last_index': 0,
        }

    def test_dependency_run(self, task):
        """
        AlwaysRebuild should indicate rebuilding task every time. NoRebuild
        should not indicate rebuilding at any time. This test tests report for
        dependencies.
        """
        task.add_dependency(AlwaysRebuild())
        task.add_dependency(NoRebuild())

        task.run()

        assert task.report == {
            'baelfire.task.tests.test_tasks.ExampleTask': {
                'dependencies': [
                    {
                        'builded': True,
                        'index': 0,
                        'should_build': True,
                        'phase_validation': True,
                        'success': True,
                        'name': 'baelfire.dependencies.dependency.AlwaysRebuild',
                    },
                    {
                        'builded': True,
                        'index': 1,
                        'should_build': False,
                        'phase_validation': True,
                        'success': True,
                        'name': 'baelfire.dependencies.dependency.NoRebuild',
                    },
                ],
                'needtorun': True,
                'runned': True,
                'success': True,
            },
            'last_index': 2,
        }

    def test_exception(self, task):
        """
        .report should make success to false, when task building raise an
        error.
        """
        task = ExampleFailingTask()

        with raises(RuntimeError):
            task.run()

        assert task.report == {
            'baelfire.task.tests.test_tasks.ExampleFailingTask': {
                'dependencies': [
                    {
                        'builded': True,
                        'index': 0,
                        'should_build': True,
                        'phase_validation': True,
                        'success': True,
                        'name': 'baelfire.dependencies.dependency.AlwaysRebuild',
                    },
                ],
                'needtorun': True,
                'runned': True,
                'success': False,
            },
            'last_index': 1,
        }

    def test_data_parrenting(self):
        """
        When task is a child of another, it should share this properties:
            - settings
            - paths
            - report
        """
        parent = ExampleParent(ExampleCore())
        child = ExampleChild()
        child.add_dependency(AlwaysRebuild())
        parent.add_dependency(TaskDependency(child))

        parent.run()

        assert parent._data == child._data
        assert parent.report == {
            'baelfire.task.tests.test_tasks.ExampleChild': {
                'dependencies': [
                    {
                        'builded': True,
                        'index': 1,
                        'should_build': True,
                        'phase_validation': True,
                        'success': True,
                        'name': 'baelfire.dependencies.dependency.AlwaysRebuild',
                    },
                ],
                'needtorun': True,
                'runned': True,
                'success': True,
            },
            'baelfire.task.tests.test_tasks.ExampleParent': {
                'dependencies': [
                    {
                        'builded': True,
                        'index': 0,
                        'phase_validation': True,
                        'should_build': True,
                        'success': True,
                        'task': 'baelfire.task.tests.test_tasks.ExampleChild',
                        'name': 'baelfire.dependencies.task.TaskDependency',
                    }
                ],
                'needtorun': True,
                'runned': True,
                'success': True,
            },
            'last_index': 2,
        }

    def test_saving(self):
        """
        .save_report should save report to a file with yaml
        """
        task = ExampleFailingTask()

        with raises(RuntimeError):
            task.run()

        task.save_report()

        data = load(open(task.paths.get('report'), 'r').read())

        assert data == {
            'baelfire.task.tests.test_tasks.ExampleFailingTask': {
                'dependencies': [
                    {
                        'builded': True,
                        'index': 0,
                        'should_build': True,
                        'phase_validation': True,
                        'success': True,
                        'name': 'baelfire.dependencies.dependency.AlwaysRebuild',
                    },
                ],
                'needtorun': True,
                'runned': True,
                'success': False,
            },
            'last_index': 1,
        }
