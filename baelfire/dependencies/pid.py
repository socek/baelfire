import os

from .dependency import Dependency


class PidFileIsRunning(Dependency):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def get_pid(self):
        with open(self.path, 'r') as pidfile:
            return int(pidfile.read())

    def is_running(self):
        try:
            os.kill(self.get_pid(), 0)
        except OSError:
            return False
        else:
            return True

    def make(self):
        return self.is_running()


class PidFileIsNotRunning(PidFileIsRunning):

    def make(self):
        return not self.is_running()
