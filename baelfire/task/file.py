from baelfire.dependencies.file import FileDoesNotExists
from baelfire.task.task import Task


class FileTask(Task):
    """
    Task which operates on files.

    Need to implement ``FileTask.output_name`` parameter.
    """

    @property
    def output(self):
        return self.paths.get(self.output_name)

    def create_dependecies(self):
        try:
            self.build_if(FileDoesNotExists(self.output_name))
        except AttributeError:
            self.build_if(FileDoesNotExists(raw_path=self.output))
