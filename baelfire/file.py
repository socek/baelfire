from .dependencies.file import FileDoesNotExists
from .task import Task


class FileTask(Task):

    @property
    def output(self):
        return self.paths[self.output_name]

    def create_dependecies(self):
        self.add_dependency(FileDoesNotExists(self.output_name))
