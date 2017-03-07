from .dependency import Dependency


class TaskDependency(Dependency):
    """
    Trigger build parent task if assigned task has changed.
    """

    def __init__(self, task):
        super(TaskDependency, self).__init__()
        self.task = task

    def phase_init(self):
        super(TaskDependency, self).phase_init()
        self.task = self.parent.top_core.prepere_task(self.task)
        self.task.phase_init()
        self.myreport['task'] = self.task.name

    def phase_data(self):
        super(TaskDependency, self).phase_data()
        self.task.phase_data()

    def set_parent(self, parent):
        super(TaskDependency, self).set_parent(parent)
        self.task.set_parent(parent)

    def should_build(self):
        return self.task.phase_validation()

    def build(self):
        self.task.phase_dependencies_build()
        self.task.phase_build()


class RunBefore(TaskDependency):
    """
    Build assigned task, but do not affect dependency checking.
    """

    def should_build(self):
        super(RunBefore, self).should_build()
        return False
