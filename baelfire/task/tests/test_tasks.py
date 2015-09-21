from pytest import fixture
from pytest import raises

from baelfire.task import Task
from baelfire.dependencies import AlwaysRebuild
from baelfire.dependencies import TaskDependency
from baelfire.dependencies.dependency import NoRebuild


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

    def phase_settings(self):
        super().phase_settings()
        self.settings['child'] = '2'
        self.paths['child'] = 'child.txt'

    def build(self):
        self._data = {
            'settings': {
                'child': self.settings['child'],
                'parent': self.settings['parent']
            },
            'paths': {
                'child': self.paths['child'],
                'parent': self.paths['parent'],
            },
        }


class ExampleParent(ExampleTask):

    def phase_settings(self):
        super().phase_settings()
        self.settings['parent'] = '1'
        self.paths['parent'] = 'parent.txt'

    def build(self):
        self._data = {
            'settings': {
                'child': self.settings['child'],
                'parent': self.settings['parent']
            },
            'paths': {
                'child': self.paths['child'],
                'parent': self.paths['parent'],
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

        assert task.datalog == {
            'baelfire.task.tests.test_tasks.ExampleTask': {
                'dependencies': {},
                'dependencies_run': [],
                'needtorun': False,
                'runned': False,
                'success': False,
            },
            'last_index': 0,
        }

    def test_dependency_run(self, task):
        """
        AlwaysRebuild should indicate rebuilding task every time. NoRebuild
        should not indicate rebuilding at any time. This test tests datalog for
        dependencies.
        """
        task.add_dependency(AlwaysRebuild())
        task.add_dependency(NoRebuild())

        task.run()

        assert task.datalog == {
            'baelfire.task.tests.test_tasks.ExampleTask': {
                'dependencies': {
                    'baelfire.dependencies.dependency.AlwaysRebuild': {
                        'builded': True,
                        'index': 0,
                        'should_build': True,
                        'phase_validation': True,
                        'success': True,
                    },
                    'baelfire.dependencies.dependency.NoRebuild': {
                        'builded': True,
                        'index': 1,
                        'should_build': False,
                        'phase_validation': True,
                        'success': True,
                    },
                },
                'dependencies_run': [
                    'baelfire.dependencies.dependency.AlwaysRebuild',
                    'baelfire.dependencies.dependency.NoRebuild',
                ],
                'needtorun': True,
                'runned': True,
                'success': True,
            },
            'last_index': 2,
        }

    def test_exception(self, task):
        """
        .datalog should make success to false, when task building raise an
        error.
        """
        task = ExampleFailingTask()

        with raises(RuntimeError):
            task.run()

        assert task.datalog == {
            'baelfire.task.tests.test_tasks.ExampleFailingTask': {
                'dependencies': {
                    'baelfire.dependencies.dependency.AlwaysRebuild': {
                        'builded': True,
                        'index': 0,
                        'should_build': True,
                        'phase_validation': True,
                        'success': True,
                    },
                },
                'dependencies_run': [
                    'baelfire.dependencies.dependency.AlwaysRebuild',
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
            - datalog
        """
        parent = ExampleParent()
        child = ExampleChild()
        child.add_dependency(AlwaysRebuild())
        parent.add_dependency(TaskDependency(child))

        parent.run()

        assert parent._data == child._data
        assert parent.datalog == {
            'baelfire.task.tests.test_tasks.ExampleChild': {
                'dependencies': {
                    'baelfire.dependencies.dependency.AlwaysRebuild': {
                        'builded': True,
                        'index': 1,
                        'should_build': True,
                        'phase_validation': True,
                        'success': True,
                    },
                },
                'dependencies_run': [
                    'baelfire.dependencies.dependency.AlwaysRebuild',
                ],
                'needtorun': True,
                'runned': True,
                'success': True,
            },
            'baelfire.task.tests.test_tasks.ExampleParent': {
                'dependencies': {
                    'baelfire.dependencies.task.TaskDependency': {
                        'builded': True,
                        'index': 0,
                        'phase_validation': True,
                        'should_build': True,
                        'success': True,
                    }
                },
                'dependencies_run': [
                    'baelfire.dependencies.task.TaskDependency',
                ],
                'needtorun': True,
                'runned': True,
                'success': True
            },
            'last_index': 2,
        }
