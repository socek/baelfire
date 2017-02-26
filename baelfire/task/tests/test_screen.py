from mock import patch
from pytest import fixture
from pytest import raises
from pytest import yield_fixture

from baelfire.task.screen import AttachScreenTask
from baelfire.task.screen import ScreenCore
from baelfire.task.screen import ScreenTask


class ExampleScreenTask(ScreenTask):
    screen_name = 'halp'

    def create_dependecies(self):
        pass


class ExampleAttachScreenTask(AttachScreenTask):
    detached_task = ExampleScreenTask


class ScreenFixtures(object):

    @yield_fixture
    def mpopen(self, task):
        with patch.object(task, 'popen') as mock:
            yield mock

    @fixture
    def core(self):
        core = ScreenCore()
        core.init()
        core.phase_settings()
        return core


class TestScreenTask(ScreenFixtures):

    @fixture
    def task(self, core):
        return ExampleScreenTask(core)

    def test_screen_run_without_name(self, task, mpopen):
        task.screen_name = None
        assert task._screen_run(['arg'], kw='arg2') == mpopen.return_value
        mpopen.assert_called_once_with(
            ['/usr/bin/screen -dm arg'],
            kw='arg2')

    def test_screen_run_with_name(self, task, mpopen):
        assert task._screen_run(['arg'], kw='arg2') == mpopen.return_value
        mpopen.assert_called_once_with(
            ['/usr/bin/screen -dmS halp arg'],
            kw='arg2')


class TestAttachScreenTask(ScreenFixtures):

    @fixture
    def task(self, core, mrun_before):
        return ExampleAttachScreenTask(core)

    @yield_fixture
    def mrun_before(self):
        with patch('baelfire.task.screen.RunBefore') as mock:
            yield mock

    def test_no_detached_task_configured(self):
        with raises(AssertionError):
            AttachScreenTask()

    def test_screen_attach(self, task, mpopen, mrun_before):
        task.run()
        mpopen.assert_called_once_with(
            ['/usr/bin/screen -r halp'])
        mrun_before.assert_called_once_with(task._detached_task)
