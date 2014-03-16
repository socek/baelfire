from importlib import import_module

from ..command import Command
from ..init.models import InitFile
from baelfire.error import OnlyOneTaskInARow


class RunTask(Command):

    def __init__(self):
        super().__init__('-t',
                         '--tasks',
                         nargs='+',
                         help='Run tasks')

    def get_recipe(self):
        """Gets recipe from command switch or init file."""
        if 'recipe' in self.raw_args:
            return import_module(self.raw_args['recipe']).recipe
        else:
            initfile = InitFile()
            if initfile.is_present():
                initfile.load()
                return initfile.get_recipe()()
        return None

    def gather_tasks(self):
        """Assign command line arguments to a tasks and produce tasks list."""
        self.run_list = []
        task_paths = []
        for taskurl in self.args:
            task = self.recipe.get_task(taskurl)

            task_path = task.get_path()
            if task_path in task_paths:
                raise OnlyOneTaskInARow(task_path)
            task_paths.append(task_path)

            self.run_list.append(task)

    def run_tasks(self):
        for task in self.run_list:
            if not task.was_runned():
                task.run()

    def make(self):
        self.recipe = self.get_recipe()
        self.gather_tasks()
        self.run_tasks()
