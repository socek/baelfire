class TaskMustHaveOutputFile(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Error: Taks must have output_file setted: %s' % (self.name)


class CouldNotCreateFile(Exception):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return 'Error: Could not create file %s' % (self.filename)


class TaskNotFound(Exception):

    def __init__(self, task):
        self.task = task

    def __str__(self):
        return 'Error: Task "%s" can not be found!' % (self.task)


class OnlyOneTaskInARow(Exception):

    def __init__(self, task):
        self.task = task

    def __str__(self):
        return 'Error: Task "%s" can be run only once!' % (self.task)
