from mock import MagicMock

from baelfire.dependencies.task import TaskRebuilded
from baelfire.dependencies.task import RunTask


class TestRunTask(object):

    def test_fail(self):
        """
        RunTask should run linked task, but should not affect dependency
        validating.
        """
        task = MagicMock()
        dependency = RunTask(task)

        assert dependency.should_build() is False


class TestTaskRebuilded(object):

    def test_fail(self):
        """
        TaskRebuilded should run linked task, but should not affect dependency
        validating.
        """
        task = MagicMock()
        dependency = TaskRebuilded(task)

        assert dependency.should_build() is task.phase_validation.return_value
