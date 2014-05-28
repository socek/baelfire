from os import path


from ..command import Command
from .models import InitFile
from .error import RecipePackageNotValidError
from baelfire.error import RecipeNotFoundError


class Init(Command):

    def __init__(self):
        super().__init__('-i',
                         '--init',
                         nargs='+',
                         help='Inits package.')

    def validate_package(self):
        try:
            self.initfile.get_recipe()
        except RecipeNotFoundError:
            raise RecipePackageNotValidError(3, self.initfile.package_url)

    def validate_setup(self):
        if self.initfile.setup_path is None:
            return
        if not path.exists(self.initfile.setup_path):
            raise RecipePackageNotValidError(2, self.initfile.setup_path)

    def make(self):
        self.initfile = InitFile()
        self.initfile.assign(*self.args)
        try:
            self.validate_package()
            self.validate_setup()

            self.initfile.install_dependencies()
            self.initfile.save()
        except RecipePackageNotValidError as er:
            print(er)
