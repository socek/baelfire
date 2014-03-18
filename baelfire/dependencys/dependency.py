class Dependency(object):

    def __init__(self):
        self.task = None
        self.parent = None

    @property
    def name(self):
        """Returns class name"""
        return self.__class__.__name__

    def assign_task(self, task):
        self.task = task

    def assign_parent(self, parent):
        self.parent = parent

    def run_parent(self):
        if self.parent is not None:
            self.parent.run()

    def validate_task(self):
        pass

    def validate_parent(self):
        pass

    def validate_dependency(self):
        pass

    def _log_method(self, name):
        """Logs method to a logdata. Sets true if no exception raised."""
        self.logdata[name] = False
        method = getattr(self, name)
        result = method()
        self.logdata[name] = True
        return result

    def __call__(self):
        self.logdata = {}
        self._log_method('validate_task')
        self._log_method('validate_parent')
        self._log_method('validate_dependency')
        self._log_method('run_parent')
        return self._log_method('make')

    def logme(self):
        self.task.recipe.data_log.add_dependecy(self.task, self, self.logdata)


class AlwaysRebuild(Dependency):

    def make(self):
        return True
