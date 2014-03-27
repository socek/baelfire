from .dependency import Dependency
from baelfire.error import TaskMustHaveOutputFileError, CouldNotCreateFileError
from os.path import exists, getmtime


class FileDependency(Dependency):

    def __init__(self, filenames):
        super().__init__()
        if type(filenames) is str:
            self.filenames = [filenames]
        elif type(filenames) in (list, tuple):
            self.filenames = filenames
        else:
            raise AttributeError('filenames should be list, tuple or string')

    def get_filenames(self):
        return self.filenames

    def _add_log_data(self):
        super()._add_log_data()
        self.logdata['filenames'] = self.filenames


class FileChanged(FileDependency):

    def validate_task(self):
        if self.task.get_output_file() is None:
            raise TaskMustHaveOutputFileError(self.task.get_path())

    def validate_dependency(self):
        for filename in self.get_filenames():
            if not exists(filename):
                raise CouldNotCreateFileError(filename)

    def is_destination_file_older(self, source, destination):
        return exists(source) and getmtime(source) > getmtime(destination)

    def make(self):
        for filename in self.get_filenames():
            if not self.is_destination_file_older(
                    self.task.get_output_file(),
                    filename):
                return True
        return False


class ParentFileChanged(FileChanged):

    def __init__(self, parent):
        super().__init__([])
        self.assign_parent(parent)

    def validate_dependency(self):
        # no need to check filenames here
        pass

    def get_filenames(self):
        return [self.parent.get_output_file()]


class FileDoesNotExists(FileDependency):

    def make(self):
        for filename in self.get_filenames():
            if not exists(filename):
                return True
        return False
