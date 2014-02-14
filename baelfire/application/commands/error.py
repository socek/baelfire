class RecipePackageNotValidError(Exception):

    codes = {
        1: 'package does not exist',
        2: 'no setup.py file found',
        3: 'no recipe found. Please create recipe var in setup.py',
    }

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return '%s: %s' % (self.codes[self.code], self.name)
