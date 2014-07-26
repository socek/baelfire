from time import sleep
from mock import MagicMock
from tempfile import NamedTemporaryFile

from soktest import TestCase

from ..dependency import Dependency
from ..file import (FileChanged,
                    FileDoesNotExists,
                    FileDependency,
                    ParentFileChanged,
                    PathsBasedFileDoesNotExists,
                    PathsBasedFileChanged)
from baelfire.error import TaskMustHaveOutputFileError, CouldNotCreateFileError
from baelfire.tests.test_task import ExampleTask as ExampleTaskBase, Task


PREFIX = 'baelfire.dependencies.file.'


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


class FileDependencyTest(TestCase):

    def test_init_list(self):
        """Should assign filenames."""
        dependency = FileDependency(['something'])
        self.assertEqual(['something'], dependency.filenames)

    def test_init_string(self):
        """Should put string into list and assign it."""
        dependency = FileDependency('something')
        self.assertEqual(['something'], dependency.filenames)

    def test_init_error(self):
        """Should raise AttributeError when no list, tuple or string
        provided"""
        self.assertRaises(AttributeError, FileDependency, 13)

    def test_logme(self):
        dependency = FileDependency(['something'])
        dependency.task = MagicMock()
        dependency.logme()

        self.assertEqual(
            {'filenames': ['something'], 'runned': False},
            dependency.logdata)


class FileChangedTest(TestCase):

    def setUp(self):
        super().setUp()
        self.dependency = FileChanged(['example_file'])

    def test_validate_task_error(self):
        """Should throw TaskMustHaveOutputFileError when task has no output
        file."""
        task = Task()
        task.recipe = MagicMock()
        task.recipe.prefix = ''
        self.dependency.assign_task(task)
        self.assertRaises(
            TaskMustHaveOutputFileError,
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
            CouldNotCreateFileError,
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

    def test_is_destination_file_older_when_no_file(self):
        """Should return true if task file does not exists."""
        destination = NamedTemporaryFile(delete=False).name
        sleep(0.01)
        source = NamedTemporaryFile().name

        result = self.dependency.is_destination_file_older(
            source,
            destination)
        self.assertEqual(False, result)

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
        self.set_filename(destination)

        self.assertEqual(True, self.dependency())

    def test_make_file_not_changed(self):
        """Should return False if task file is newer then dependency file."""
        destination = NamedTemporaryFile(delete=False).name
        self.set_filename(destination)

        sleep(0.01)
        task = ExampleTask()
        task.get_output_file()
        self.dependency.assign_task(task)

        self.assertEqual(False, self.dependency())

    def set_filename(self, filename):
        self.dependency.filenames = [filename]


class PathsBasedFileChangedTest(FileChangedTest):

    def setUp(self):
        super().setUp()
        self.paths = {'filename': 'example_file'}
        self.dependency = PathsBasedFileChanged(self.paths, ['filename'])

    def set_filename(self, filename):
        self.paths['filename'] = filename


class FileDoesNotExistsTest(TestCase):

    def test_success(self):
        """Should return True, if on of file does not exist."""
        dependency = FileDoesNotExists(['/tmp/something'])
        self.assertEqual(True, dependency())

    def test_fail(self):
        """Should return False, if all the files exists."""
        destination = NamedTemporaryFile(delete=False).name
        dependency = FileDoesNotExists([destination])
        self.assertEqual(False, dependency())


class PathsBasedFileDoesNotExistsTest(TestCase):

    def test_success(self):
        """Should return True, if on of file does not exist."""
        paths = {'filename': '/tmp/something'}
        dependency = PathsBasedFileDoesNotExists(paths, 'filename')
        self.assertEqual(True, dependency())

    def test_fail(self):
        """Should return False, if all the files exists."""
        destination = NamedTemporaryFile(delete=False).name
        paths = {'filename': destination}
        dependency = PathsBasedFileDoesNotExists(paths, 'filename')
        self.assertEqual(False, dependency())


class ParentFileChangedTest(TestCase):

    def setUp(self):
        super().setUp()
        self.parent = ExampleTask()
        self.dependency = ParentFileChanged(self.parent)

    def test_validate_dependency(self):
        """Should do nothing. (sic!)"""
        self.assertEqual(None, self.dependency.validate_dependency())

    def test_get_filenames(self):
        """Should return output_file from parent"""
        self.assertEqual(
            [self.parent.get_output_file()],
            self.dependency.get_filenames())

    def test_logme(self):
        self.dependency.task = MagicMock()
        self.dependency.logme()

        self.assertEqual(
            {
                'filenames': [],
                'parent': {
                    'file': self.parent.filename,
                    'name': 'ExampleTask',
                    'path': 'baelfire.dependencies.tests'
                            '.test_file:ExampleTask'},
                'runned': False},
            self.dependency.logdata)
