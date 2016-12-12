import os

from .dependency import Dependency


class PidIsRunning(Dependency):
    """
    Trigger build if pid is running.
    """

    def __init__(self, pid=None, pid_file_name=None, pid_file_path=None):
        super(PidIsRunning, self).__init__()
        self.pid = pid
        self.pid_file_name = pid_file_name
        self.pid_file_path = pid_file_path

    def get_pid(self):
        if self.pid:
            return self.pid
        elif self.pid_file_name:
            return self._get_pid_from_file(self.paths[self.pid_file_name])
        else:
            return self._get_pid_from_file(self.pid_file_path)

    def _get_pid_from_file(self, path):
        with open(path, 'r') as pidfile:
            return int(pidfile.read())

    def is_running(self):
        try:
            os.kill(self.get_pid(), 0)
            return True
        except OSError:
            return False

    def should_build(self):
        return self.is_running()


class PidIsNotRunning(PidIsRunning):
    """
    Trigger build if pid is not running.
    """

    def should_build(self):
        return not self.is_running()
