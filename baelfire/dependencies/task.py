from .dependency import Dependency


class TaskDependency(Dependency):

    """
    Should build parent task if assigned task has changed.
    """

    def __init__(self, task):
        super().__init__()
        self.task = task

    def phase_init(self):
        super().phase_init()
        self.task.phase_init()

    def phase_data(self):
        super().phase_data()
        self.task.phase_data()

    def phase_settings(self):
        super().phase_settings()
        self.task.phase_settings()

    def set_parent(self, parent):
        super().set_parent(parent)
        self.task.set_parent(parent)

    def should_build(self):
        return self.task.phase_validation()

    def build(self):
        self.task.phase_build()
        self.task.phase_mybuild()


class LinkTask(TaskDependency):

    """
    Build assigned task, but do not affect dependency checking.
    """

    def should_build(self):
        super().should_build()
        return False
