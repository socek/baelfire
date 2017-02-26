from subprocess import PIPE
from subprocess import Popen
import re

from .dependency import Dependency


class ScreenIsNotRunning(Dependency):
    regex = re.compile(r'^\s*([^\.]*)\.([^\s]+)\s*\((\w+)\)$', re.UNICODE)

    def __init__(self, screen_name=None):
        super(ScreenIsNotRunning, self).__init__()
        self._screen_name = screen_name

    def _list_screen(self):
        cmd = self.paths.get('exe:screen') + ' -list'
        spp = Popen([cmd], shell=True, stdout=PIPE)
        spp.wait()
        return spp.stdout

    def get_screens(self):
        for line in self._list_screen().readlines():
            line = line.decode()
            try:
                data = self.regex.findall(str(line))[0]
                yield {
                    'pid': int(data[0]),
                    'name': data[1],
                    'status': data[2],
                }
            except IndexError:
                pass

    def should_build(self):
        for screen in self.get_screens():
            if screen['name'] == self.screen_name:
                return False
        return True

    @property
    def screen_name(self):
        return self._screen_name or self.parent.screen_name
