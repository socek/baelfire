from ..command import Command
from baelfire.error import OnlyOneTaskInARowError, CommandAborted


class RunTask(Command):

    def __init__(self):
        super().__init__(nargs='*',
                         help='List of task to do.')

    def gather_tasks(self):
        """Assign command line arguments to a tasks and produce tasks list."""
        self.run_list = []
        task_paths = []
        for taskurl in self.args:
            task = self.recipe.get_task(taskurl)

            task_path = task.get_path()
            if task_path in task_paths:
                raise OnlyOneTaskInARowError(task_path)
            task_paths.append(task_path)

            self.run_list.append(task)

    def run_tasks(self):
        for task in self.run_list:
            if not task.was_runned():
                task.run()

    def make(self):
        self.recipe = self.get_recipe()
        self.gather_tasks()
        try:
            self.run_tasks()
        except CommandAborted:
            self.recipe.log.warning('>> Command aborted!')
        finally:
            self.recipe.data_log.save()
