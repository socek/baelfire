from os import path


from ..command import Command
from .models import InitFile
from .error import RecipePackageNotValidError


class Init(Command):

    def __init__(self):
        super().__init__('init',
                         '-i',
                         '--init',
                         dest='init',
                         nargs=1,
                         help='Inits package.')

    def module_exists(self, module_path):
        if path.exists(path.join(module_path, '__init__.py')):
            return True
        for sufix in ['.py', '.pyc', '.pyo']:
            if path.exists(module_path + sufix):
                return True
        return False

    def validate_package(self, name):
        if not path.exists(name):
            raise RecipePackageNotValidError(1, name)

        setup_path = path.join(name, 'setup')
        if not self.module_exists(setup_path):
            raise RecipePackageNotValidError(2, name)

        self.initfile = InitFile()
        self.initfile.package = name
        try:
            self.initfile.get_recipe()
        except AttributeError:
            raise RecipePackageNotValidError(3, name)

    def make(self):
        try:
            package = self.args[0]
            self.validate_package(package)
            self.initfile.save()
        except RecipePackageNotValidError as er:
            print(er)
