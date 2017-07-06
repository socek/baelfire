from mock import MagicMock
from mock import patch
from mock import sentinel
from pytest import fixture
from pytest import mark
from pytest import raises
from pytest import yield_fixture
from yaml import load

from baelfire.core import Core
from baelfire.dependencies import AlwaysTrue
from baelfire.dependencies.dependency import AlwaysFalse
from baelfire.dependencies.task import TaskRebuilded
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
        self.build_if(AlwaysTrue())

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

    @yield_fixture
    def mrun_task(self):
        with patch('baelfire.task.task.RunTask') as mock:
            yield mock

    @yield_fixture
    def mopen(self):
        with patch('baelfire.task.task.open') as mock:
            yield mock

    @yield_fixture
    def mutime(self):
        with patch('baelfire.task.task.utime') as mock:
            yield mock

    @yield_fixture
    def mpaths(self, task):
        task.core.paths = MagicMock()
        return task.core.paths

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
        AlwaysTrue should indicate rebuilding task every time. AlwaysFalse
        should not indicate rebuilding at any time. This test tests report for
        dependencies.
        """
        task.build_if(AlwaysTrue())
        task.build_if(AlwaysFalse())

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
                        'name': 'baelfire.dependencies.dependency.AlwaysTrue',
                    },
                    {
                        'builded': True,
                        'index': 1,
                        'should_build': False,
                        'phase_validation': True,
                        'success': True,
                        'name': 'baelfire.dependencies.dependency.AlwaysFalse',
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
                        'name': 'baelfire.dependencies.dependency.AlwaysTrue',
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
        child.build_if(AlwaysTrue())
        parent.build_if(TaskRebuilded(child))

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
                        'name': 'baelfire.dependencies.dependency.AlwaysTrue',
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
                        'name': 'baelfire.dependencies.task.TaskRebuilded',
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
                        'name': 'baelfire.dependencies.dependency.AlwaysTrue',
                    },
                ],
                'needtorun': True,
                'runned': True,
                'success': False,
            },
            'last_index': 1,
        }

    def test_run_before(self, task, mrun_task):
        """
        .run_before should add RunTask dependency to the dependency list.
        """
        child_task = MagicMock()
        task.run_before(child_task)

        assert task._dependencies == [mrun_task.return_value]
        mrun_task.assert_called_once_with(child_task)
        mrun_task.return_value.set_parent.assert_called_once_with(task)

    @mark.parametrize(
        'file_name, file_path, should_validate',
        [
            [None, None, False],
            [True, None, True],
            [None, True, True],
            [True, True, False],
        ]
    )
    def test_touch_assertion(self, task, file_name, file_path, should_validate, mopen, mutime, mpaths):
        """
        .touch should allow only setting file_name xor file_path.
        """
        if should_validate:
            task.touch(file_name=file_name, file_path=file_path)
        else:
            with raises(AssertionError):
                task.touch(file_name=file_name, file_path=file_path)

    @mark.parametrize(
        'file_name, file_path',
        [
            ['file_name', None],
            [None, 'file_path'],
        ]
    )
    def test_touch_get_path(self, task, file_name, file_path, mopen, mutime, mpaths):
        """
        .touch should get path from paths or get file_path as a raw path.
        """
        task.touch(file_name=file_name, file_path=file_path, times=sentinel.times)
        if file_name:
            mopen.assert_called_once_with(mpaths.get.return_value, 'a')
            mutime.assert_called_once_with(mpaths.get.return_value, sentinel.times)
        if file_path:
            mopen.assert_called_once_with(file_path, 'a')
            mutime.assert_called_once_with(file_path, sentinel.times)
