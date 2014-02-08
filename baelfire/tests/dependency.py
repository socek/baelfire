from tempfile import NamedTemporaryFile
from time import sleep

from soktest import TestCase

from baelfire.error import TaskMustHaveOutputFile, CouldNotCreateFile
from .task import ExampleTask as ExampleTaskBase, Task
from ..dependencys import Dependency, FileChanged

PREFIX = 'baelfire.dependencys.'


class ExampleTask(ExampleTaskBase):

    def get_output_file(self):
        self.filename = getattr(
            self, 'filename', NamedTemporaryFile(delete=False).name)
        return self.filename


class ExampleDependency(Dependency):

    def __init__(self):
        super().__init__()
        self.running = []

    def validate_task(self):
        self.running.append('validate_task')

    def validate_parent(self):
        self.running.append('validate_parent')

    def validate_dependency(self):
        self.running.append('validate_dependency')

    def make(self):
        self.running.append('make')
        return 'make'


class DependencyTest(TestCase):

    def setUp(self):
        super().setUp()
        self.task = ExampleTask()
        self.dependency = ExampleDependency()
        self.dependency.assign_task(self.task)

    def test_init(self):
        dependency = Dependency()

        self.assertEqual(None, dependency.task)
        self.assertEqual(None, dependency.parent)

    def test_assign_task(self):
        """Should assign task"""
        self.assertEqual(self.task, self.dependency.task)

    def test_assign_parent(self):
        """Should assign parent"""
        task = ExampleTask()
        self.dependency.assign_parent(task)
        self.assertEqual(task, self.dependency.parent)

    def test_call(self):
        """Should run validation of task, parent and then run make method."""
        self.assertEqual('make', self.dependency())
        self.assertEqual(
            ['validate_task', 'validate_parent',
                'validate_dependency', 'make'],
            self.dependency.running)


class FileChangedTest(TestCase):

    def setUp(self):
        super().setUp()
        self.dependency = FileChanged(['example_file'])

    def test_validate_task_error(self):
        """Should throw TaskMustHaveOutputFile when task has no output file."""
        task = Task()
        self.dependency.assign_task(task)
        self.assertRaises(
            TaskMustHaveOutputFile,
            self.dependency.validate_task)

    def test_validate_task(self):
        """Should return None when task is valid."""
        task = ExampleTask()
        self.dependency.assign_task(task)
        self.assertEqual(None, self.dependency.validate_task())

    def test_validate_dependency_error(self):
        """Should raise error when one of the file in filenames do not
        exists."""
        self.add_mock(PREFIX + 'exists')
        self.mocks['exists'].return_value = False

        self.assertRaises(
            CouldNotCreateFile,
            self.dependency.validate_dependency)

    def test_validate_dependency(self):
        """Should return None when all files exists."""
        self.add_mock(PREFIX + 'exists')
        self.mocks['exists'].return_value = True

        self.assertEqual(None, self.dependency.validate_dependency())

    def test_is_destination_file_older_success(self):
        """Should return true if destination path is older"""
        destination = NamedTemporaryFile(delete=False).name
        sleep(0.01)
        source = NamedTemporaryFile(delete=False).name

        result = self.dependency.is_destination_file_older(
            source,
            destination)
        self.assertEqual(True, result)

    def test_is_destination_file_older_fail(self):
        """Should return false if source path is older"""
        source = NamedTemporaryFile(delete=False).name
        sleep(0.01)
        destination = NamedTemporaryFile(delete=False).name

        result = self.dependency.is_destination_file_older(
            source,
            destination)
        self.assertEqual(False, result)

    def test_make_file_changed(self):
        """Should return True if task file is older then dependency file."""
        task = ExampleTask()
        task.get_output_file()
        self.dependency.assign_task(task)

        sleep(0.01)
        destination = NamedTemporaryFile(delete=False).name
        self.dependency.filenames = [destination]

        self.assertEqual(True, self.dependency())

    def test_make_file_not_changed(self):
        """Should return False if task file is newer then dependency file."""
        destination = NamedTemporaryFile(delete=False).name
        self.dependency.filenames = [destination]

        sleep(0.01)
        task = ExampleTask()
        task.get_output_file()
        self.dependency.assign_task(task)

        self.assertEqual(False, self.dependency())
