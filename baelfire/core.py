from morfdict import Paths
from morfdict import StringDict


class TaskInheritance(object):

    def __init__(self, base_cls, child_cls, migration=None):
        self.base_cls = base_cls
        self.child_cls = child_cls
        self.migration = migration or self._default_migration

    def is_ready_to_migrate(self, task):
        return self.base_cls == task.__class__

    def migrate(self, task):
        return self.migration(task, self.child_cls)

    def _default_migration(self, task, child_cls):
        return child_cls()

    def is_doubled(self, base_cls):
        return self.base_cls == base_cls


class Core(object):

    def __init__(self):
        self.inheritance = []
        self.make_task_inheritance()

    def init(self):
        self.settings = StringDict()
        self.paths = Paths()
        self.report = {'last_index': 0}

    def phase_settings(self):
        pass

    def prepere_task(self, task):
        for inheritance in self.inheritance:
            if inheritance.is_ready_to_migrate(task):
                old_parent = task.parent
                task = inheritance.migrate(task)
                task.set_parent(old_parent)
                return task
        return task

    def make_task_inheritance(self):
        pass

    def add_task_inheritance(self, base_cls, child_cls, migration=None):
        self._remove_old_inheritance(base_cls)
        self.inheritance.append(
            TaskInheritance(base_cls, child_cls, migration))

    def _remove_old_inheritance(self, base_cls):
        for inheritance in list(self.inheritance):
            if inheritance.is_doubled(base_cls):
                self.inheritance.remove(inheritance)
                return
