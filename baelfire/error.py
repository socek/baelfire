class TaskMustHaveOutputFileError(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Error: Taks must have output_file setted: %s' % (self.name)


class CouldNotCreateFileError(Exception):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return 'Error: Could not create file %s' % (self.filename)


class TaskNotFoundError(Exception):

    def __init__(self, task):
        self.task = task

    def __str__(self):
        return 'Error: Task "%s" can not be found!' % (self.task)


class OnlyOneTaskInARowError(Exception):

    def __init__(self, task):
        self.task = task

    def __str__(self):
        return 'Error: Task "%s" can be run only once!' % (self.task)


class CommandError(Exception):

    def __init__(self, number, text=''):
        self.number = number
        self.text = text

    def __str__(self):
        return 'Error: Command error (%d): %s' % (self.number, self.text)


class CommandAborted(Exception):
    pass
