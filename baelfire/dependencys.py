from baelfire.error import TaskMustHaveOutputFile, CouldNotCreateFile
from os.path import exists


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
        self.filenames = filenames


class FileChanged(FileDependency):

    def validate_task(self):
        if self.task.get_output_file() is None:
            raise TaskMustHaveOutputFile(self.task.get_path())

    def validate_dependency(self):
        for filename in self.filenames:
            if not exists(filename):
                raise CouldNotCreateFile(filename)

    # def make(self):
    #     for filename in self.filenames:
    #         if not os.path.exists(filename):
