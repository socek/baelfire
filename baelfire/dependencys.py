from baelfire.error import TaskMustHaveOutputFile, CouldNotCreateFile
from os.path import exists, getmtime


class Dependency(object):

    def __init__(self):
        self.task = None
        self.parent = None

    def assign_task(self, task):
        self.task = task

    def assign_parent(self, parent):
        self.parent = parent

    def validate_task(self):
        pass

    def validate_parent(self):
        pass

    def validate_dependency(self):
        pass

    def __call__(self):
        self.validate_task()
        self.validate_parent()
        self.validate_dependency()
        return self.make()


class FileDependency(Dependency):

    def __init__(self, filenames):
        super().__init__()
        if type(filenames) is str:
            self.filenames = [filenames]
        elif type(filenames) in (list, tuple):
            self.filenames = filenames
        else:
            raise AttributeError('filenames should be list, tuple or string')


class FileChanged(FileDependency):

    def validate_task(self):
        if self.task.get_output_file() is None:
            raise TaskMustHaveOutputFile(self.task.get_path())

    def validate_dependency(self):
        for filename in self.filenames:
            if not exists(filename):
                raise CouldNotCreateFile(filename)

    def is_destination_file_older(self, source, destination):
        if getmtime(source) > getmtime(destination):
            return True
        else:
            return False

    def make(self):
        for filename in self.filenames:
            if not self.is_destination_file_older(
                    self.task.get_output_file(),
                    filename):
                return True
        return False


class FileDoesNotExists(FileDependency):

    def make(self):
        for filename in self.filenames:
            if not exists(filename):
                return True
        return False


class AlwaysRebuild(Dependency):

    def make(self):
        return True
