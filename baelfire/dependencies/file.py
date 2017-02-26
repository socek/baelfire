from os.path import exists
from os.path import getmtime

from .dependency import Dependency


class FileDependency(Dependency):
    """
    Base file dependency.
    """

    def __init__(self, name=None, raw_path=None):
        super(FileDependency, self).__init__()
        self.source_name = name
        self.raw_path = raw_path

    def phase_data(self):
        super(FileDependency, self).phase_data()
        self.myreport['filename'] = self.path

    @property
    def path(self):
        return self.raw_path or self.paths.get(self.source_name)


class FileChanged(FileDependency):
    """
    Trigger build if dependency file was changed.
    """

    def should_build(self):
        try:
            output = getmtime(self.parent.output)
        except OSError:
            return True
        try:
            source = getmtime(self.path)
        except OSError:
            return True

        return output < source


class FileExists(FileDependency):
    """
    Trigger build if dependency file exists.
    """

    def should_build(self):
        return exists(self.path)


class FileDoesNotExists(FileDependency):
    """
    Trigger build if dependency file does not exists.
    """

    def should_build(self):
        return not exists(self.path)
