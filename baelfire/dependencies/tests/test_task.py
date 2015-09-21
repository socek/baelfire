from mock import MagicMock

from ..task import RunBefore
from ..task import TaskDependency


class TestRunBefore(object):

    def test_fail(self):
        """
        RunBefore should run linked task, but should not affect dependency
        validating.
        """
        task = MagicMock()
        dependency = RunBefore(task)

        assert dependency.should_build() is False


class TestTaskDependency(object):

    def test_fail(self):
        """
        TaskDependency should run linked task, but should not affect dependency
        validating.
        """
        task = MagicMock()
        dependency = TaskDependency(task)

        assert dependency.should_build() is task.phase_validation.return_value
