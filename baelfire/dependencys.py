class Dependency(object):

    def __init__(self):
        self.task = None
        self.parent = None

    def assign_task(self, task):
        self.task = task

    def assign_parent(self, parent):
        self.parent = parent

    def validate_task(self):
        pass

    def validate_parent(self):
        pass

    def __call__(self):
        self.validate_task()
        self.validate_parent()
        return self.make()
