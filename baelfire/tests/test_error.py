from baelfire import error


class TestErrors(object):

    def test_task_must_have_output_file_error(self):
        """
        Should create TaskMustHaveOutputFileError error with name.
        """
        er = error.TaskMustHaveOutputFileError('name')
        assert str(er) == "Error: Taks must have output_file setted: name"

    def test_could_not_create_file_error(self):
        """
        Should create CouldNotCreateFileError error with filename.
        """
        er = error.CouldNotCreateFileError('filename')
        assert str(er) == 'Error: Could not create file filename'

    def test_task_not_found_error(self):
        """
        Should create TaskNotFoundError error with task name.
        """
        er = error.TaskNotFoundError('task_me')
        assert str(er) == 'Error: Task "task_me" can not be found!'

    def test_only_one_task_in_a_row_error_error(self):
        """
        Should create OnlyOneTaskInARowError error with task name.
        """
        er = error.OnlyOneTaskInARowError('task_me')
        assert str(er) == 'Error: Task "task_me" can be run only once!'

    def test_command_error(self):
        er = error.CommandError(11, 'text')
        assert str(er) == 'Error: Command error (11): text'
