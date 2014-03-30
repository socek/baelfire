from os import path


from ..command import Command
from .models import InitFile
from .error import RecipePackageNotValidError


class Init(Command):

    def __init__(self):
        super().__init__('-i',
                         '--init',
                         nargs=2,
                         help='Inits package.')

    def validate_package(self):
        try:
            self.initfile.get_recipe()
        except AttributeError:
            raise RecipePackageNotValidError(3, self.initfile.package_url)

    def validate_setup(self):
        if not path.exists(self.initfile.setup_path):
            raise RecipePackageNotValidError(2, self.initfile.setup_path)

    def make(self):
        self.initfile = InitFile()
        self.initfile.assign(*self.args)
        try:
            self.validate_package()
            self.validate_setup()

            self.initfile.install_dependencys()
        except RecipePackageNotValidError as er:
            print(er)
