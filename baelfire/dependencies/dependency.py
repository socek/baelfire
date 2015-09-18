class Dependency(object):

    @property
    def name(self):
        """
        Return name of this task.
        """
        return self.__module__ + "." + self.__class__.__name__

    def __init__(self):
        self.task = None
        self.parent = None

    def phase_init(self):
        self.mylog['should_run'] = False
        self.mylog['runned'] = False
        self.mylog['success'] = False
        self.mylog['result'] = None
        self.mylog['index'] = self.parent.get_index()

    def phase_settings(self):
        pass

    def phase_data(self):
        pass

    def phase_validation(self):
        self.mylog['should_run'] = True
        result = self.should_run()
        self.mylog['result'] = result
        return result

    def phase_run(self):
        self.mylog['runned'] = True
        self.run()
        self.mylog['success'] = True

    def set_parent(self, parent):
        self.parent = parent

    @property
    def mylog(self):
        if self.name not in self.parent.mylog['dependencies']:
            self.parent.mylog['dependencies'][self.name] = {}
        return self.parent.mylog['dependencies'][self.name]

    def run(self):
        pass


class AlwaysRebuild(Dependency):

    def should_run(self):
        return True


class NeverRebuild(Dependency):

    def should_run(self):
        return False


class TaskDependency(Dependency):

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

    def should_run(self):
        return self.task.phase_validation()

    def run(self):
        self.task.phase_myrun()


class LinkTask(TaskDependency):

    def should_run(self):
        super().should_run()
        return False
