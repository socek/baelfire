from baelfire.dependencies.dependency import Dependency


class TaskRebuilded(Dependency):
    """
    Trigger build parent task if assigned task has rebuilded.
    """

    def __init__(self, task):
        super(TaskRebuilded, self).__init__()
        self.task = task

    def phase_init(self):
        super(TaskRebuilded, self).phase_init()
        self.task = self.parent.top_core.prepere_task(self.task)
        self.task.phase_init()
        self.myreport['task'] = self.task.name

    def phase_data(self):
        super(TaskRebuilded, self).phase_data()
        self.task.phase_data()

    def set_parent(self, parent):
        super(TaskRebuilded, self).set_parent(parent)
        self.task.set_parent(parent)

    def should_build(self):
        return self.task.phase_validation()

    def build(self):
        self.task.phase_dependencies_build()
        self.task.phase_build()


class RunTask(TaskRebuilded):
    """
    Run provided task before the parent.
    """

    def should_build(self):
        super(RunTask, self).should_build()
        return False
