from mock import MagicMock
from signal import SIGKILL
from subprocess import Popen
from tempfile import NamedTemporaryFile

from ..pid import PidIsNotRunning
from ..pid import PidIsRunning


class TestPidIsRunning(object):

    def test_raw_pid(self):
        spp = Popen(['sleep 10'], shell=True)

        is_running = PidIsRunning(spp.pid)
        is_not_running = PidIsNotRunning(spp.pid)

        try:
            assert is_running.should_build() is True
            assert is_not_running.should_build() is False
        finally:
            spp.send_signal(SIGKILL)

    def test_raw_path(self):
        spp = Popen(['sleep 10'], shell=True)
        with NamedTemporaryFile(mode='w', delete=False) as data:
            data.write(str(spp.pid))

            is_running = PidIsRunning(pid_file_path=data.name)
            is_not_running = PidIsNotRunning(pid_file_path=data.name)

        try:
            assert is_running.should_build() is True
            assert is_not_running.should_build() is False
        finally:
            spp.send_signal(SIGKILL)

    def test_path_name(self):
        spp = Popen(['sleep 10'], shell=True)
        with NamedTemporaryFile(mode='w', delete=False) as data:
            data.write(str(spp.pid))
            parent = MagicMock()
            parent.paths = {'pid': data.name}
        is_running = PidIsRunning(pid_file_name='pid')
        is_running.set_parent(parent)
        is_not_running = PidIsNotRunning(pid_file_name='pid')
        is_not_running.set_parent(parent)

        try:
            assert is_running.should_build() is True
            assert is_not_running.should_build() is False
        finally:
            spp.send_signal(SIGKILL)

    def test_pid_not_exists(self):
        is_running = PidIsRunning(1231231213)
        is_not_running = PidIsNotRunning(1231231213)

        assert is_running.should_build() is False
        assert is_not_running.should_build() is True
