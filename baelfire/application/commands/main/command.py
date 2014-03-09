from ..command import Command
from ..init.models import InitFile


class RunTask(Command):

    def __init__(self):
        super().__init__('-r',
                         '--run',
                         nargs='+',
                         help='Run tasks')

    def get_recipe(self):
        """Gets recipe from command switch or init file."""
        # TODO: get recipe from command switch
        initfile = InitFile()
        if initfile.is_present():
            initfile.load()
            return initfile.get_recipe()()
        return None

    def make(self):
        recipe = self.get_recipe()
        for task in self.args:
            recipe.get_task(task)
        print('hello', self.args, recipe)
