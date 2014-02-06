from soktest import TestCase

from baelfire import error


class ErrorsTests(TestCase):

    def test_TaskMustHaveOutputFile(self):
        """Should create TaskMustHaveOutputFile error with name."""
        er = error.TaskMustHaveOutputFile('name')
        self.assertEqual(
            "Error: Taks must have output_file setted: name", str(er))

    def test_CouldNotCreateFile(self):
        """Should create CouldNotCreateFile error with filename."""
        er = error.CouldNotCreateFile('filename')
        self.assertEqual('Error: Could not create file filename', str(er))
