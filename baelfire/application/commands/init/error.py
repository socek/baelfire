class RecipePackageNotValidError(Exception):

    codes = {
        1: 'package does not exist',
        2: 'setup.py file not exist',
        3: 'no recipe found in package',
    }

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return '%s: %s' % (self.codes[self.code], self.name)


class RecipeInstallError(Exception):

    """Raised when install dependencies or tests for recipe failed."""
