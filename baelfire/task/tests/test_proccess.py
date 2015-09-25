from signal import SIGALRM

from mock import MagicMock
from mock import call
from mock import patch
from pytest import fixture
from pytest import raises
from pytest import yield_fixture

from ..process import SubprocessTask
from baelfire.error import CommandAborted
from baelfire.error import CommandError


class ExampleSubproccessTask(SubprocessTask):

    def create_dependecies(self):
        pass


class TestSubproccessTask(object):

    @fixture
    def task(self):
        return ExampleSubproccessTask()

    @yield_fixture
    def signal(self):
        with patch('baelfire.task.process.signal') as mock:
            yield mock

    @yield_fixture
    def popen(self):
        with patch('baelfire.task.process.Popen') as mock:
            yield mock

    @yield_fixture
    def send_signal(self, task):
        with patch.object(task, 'send_signal') as mock:
            yield mock

    @yield_fixture
    def task_popen(self, task):
        with patch.object(task, '_popen') as mock:
            yield mock

    @yield_fixture
    def init_signals(self, task):
        with patch.object(task, '_init_signals') as mock:
            yield mock

    def test_phase_init(self, task):
        """
        .phase_init should add .spp with None and report['aborted'] = False
        """
        task.phase_init()

        assert task.myreport['aborted'] is False
        assert task.myreport['signal'] is None

    def test_init_signals(self, task, signal):
        task._init_signals()

        signal.signal.assert_has_calls([
            call(signal.SIGABRT, task.on_signal),
            call(signal.SIGFPE, task.on_signal),
            call(signal.SIGILL, task.on_signal),
            call(signal.SIGINT, task.on_signal),
            call(signal.SIGSEGV, task.on_signal),
            call(signal.SIGTERM, task.on_signal),
        ])

    def test_send_signal_on_poll_something(self, task):
        """
        .send_signal do nothing, if spp.poll() is empty.
        spp.poll() returning something means the subprocess has ended
        """
        task.spp = MagicMock()

        task.send_signal('sig')

        task.spp.poll.assert_called_once_with()
        assert not task.spp.send_signal.called

    def test_send_signal_normal(self, task):
        """
        .send_signal should send signal if poll returned something
        """
        task.spp = MagicMock()
        task.spp.poll.return_value = None

        task.send_signal('sig')

        task.spp.poll.assert_called_once_with()
        task.spp.send_signal.assert_called_once_with('sig')

    def test_send_signal_on_error(self, task):
        """
        .send_signal should do nothing on raised OSError
        OSError means that subprocess returned error
        """
        task.spp = MagicMock()
        task.spp.poll.side_effect = OSError

        task.send_signal('sig')

        task.spp.poll.assert_called_once_with()
        assert not task.spp.send_signal.called

    def test_on_signal(self, task, send_signal):
        """
        .on_signal should update report and send signal to process when
        process exists
        """
        task.phase_init()
        task.spp = MagicMock()

        task.on_signal(SIGALRM, None)

        send_signal.assert_called_once_with(SIGALRM)
        assert task.myreport['aborted'] is True
        assert task.myreport['signal'] is SIGALRM

    def test_on_signal_with_no_spp(self, task, send_signal):
        """
        .on_signal should update report. This is sanity check.
        """
        task.phase_init()
        task.spp = None

        task.on_signal(SIGALRM, None)

        assert task.myreport['aborted'] is True
        assert task.myreport['signal'] is SIGALRM

    def test_popen(self, task, task_popen, init_signals):
        task.phase_init()
        task.spp = MagicMock()
        task.spp.returncode = 0
        task.popen('arg', kw='arg')

        init_signals.assert_called_once_with()
        task_popen.assert_called_once_with('arg', kw='arg', shell=True)

    def test_popen_on_error(self, task, task_popen, init_signals):
        task.phase_init()
        task.spp = MagicMock()
        task.myreport['aborted'] = True

        with raises(CommandAborted):
            task.popen()

        init_signals.assert_called_once_with()
        task_popen.assert_called_once_with(shell=True)

    def test_popen_on_command_error(self, task, task_popen, init_signals):
        task.phase_init()
        task.spp = MagicMock()

        with raises(CommandError):
            task.popen()

        init_signals.assert_called_once_with()
        task_popen.assert_called_once_with(shell=True)

    def test_system_popen(self, task, popen):
        task._popen('arg', kw='arg')

        popen.assert_called_once_with('arg', kw='arg')
        assert task.spp == popen.return_value
        task.spp.wait.assert_called_once_with()
