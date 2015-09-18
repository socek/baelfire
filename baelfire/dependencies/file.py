from os.path import exists
from os.path import getmtime

from .dependency import Dependency


class FileDependency(Dependency):

    def __init__(self, name):
        super().__init__()
        self.source_name = name

    def phase_data(self):
        super().phase_data()
        self.mylog['filename'] = self.path

    @property
    def path(self):
        return self.paths[self.source_name]


class FileChanged(FileDependency):

    def should_build(self):
        try:
            output = getmtime(self.parent.output)
        except FileNotFoundError:
            return True
        source = getmtime(self.path)

        return output < source


class FileDoesNotExists(FileDependency):

    def should_build(self):
        return not exists(self.path)
