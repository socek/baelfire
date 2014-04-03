from soktest import TestCase

from baelfire import error


class ErrorsTests(TestCase):

    def test_TaskMustHaveOutputFileError(self):
        """Should create TaskMustHaveOutputFileError error with name."""
        er = error.TaskMustHaveOutputFileError('name')
        self.assertEqual(
            "Error: Taks must have output_file setted: name", str(er))

    def test_CouldNotCreateFileError(self):
        """Should create CouldNotCreateFileError error with filename."""
        er = error.CouldNotCreateFileError('filename')
        self.assertEqual('Error: Could not create file filename', str(er))

    def test_TaskNotFoundError(self):
        """Should create TaskNotFoundError error with task name."""
        er = error.TaskNotFoundError('task_me')
        self.assertEqual('Error: Task "task_me" can not be found!', str(er))

    def test_OnlyOneTaskInARowErrorError(self):
        """Should create OnlyOneTaskInARowError error with task name."""
        er = error.OnlyOneTaskInARowError('task_me')
        self.assertEqual('Error: Task "task_me" can be run only once!',
                         str(er))

    def test_BadRecipePathError(self):
        er = error.BadRecipePathError()
        self.assertEqual('Error: Bad path for recipe!',
                         str(er))

    def test_RecipeNotFoundError(self):
        er = error.RecipeNotFoundError()
        self.assertEqual('Error: No recipe found!',
                         str(er))

    def test_CommandError(self):
        er = error.CommandError(11, 'text')
        self.assertEqual('Error: Command error (11): text',
                         str(er))
