from baelfire.error import TaskMustHaveOutputFile


class Dependency(object):

    def __init__(self):
        self.parent_task = None

    def assign_parent(self, parent_task):
        self.parent_task = parent_task

    def __call__(self, task):
        self.task = task
        return self.make()


class FileDependency(Dependency):

    def __init__(self, filenames):
        super().__init__()
        self.filenames = filenames


class FileChanged(FileDependency):

    def validate_task(self):
        if self.task.get_output_file() is None:
            raise TaskMustHaveOutputFile(self.task.get_path())

    def validate_parent_task(self):
        if self.parent_task is not None and \
                self.parent_task.get_output_file() is None:
            raise TaskMustHaveOutputFile(self.parent_task.get_path())

    def make(self):
        self.validate_task()
        self.validate_parent_task()
