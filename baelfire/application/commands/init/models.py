import json
from os import path


class InitFile(object):

    filename = '.bael.init'

    def __init__(self):
        self.package = None
        self.module = None

    def to_dict(self):
        return {
            'package': self.package,
        }

    def from_dict(self, data):
        self.package = data['package']

    def save(self):
        initfile = open(self.filename, 'w')
        json.dump(self.to_dict(), initfile)
        initfile.close()

    def load(self):
        initfile = open(self.filename, 'r')
        data = json.load(initfile)
        self.from_dict(data)
        initfile.close()

    def get_recipe(self):
        if self.module is None:
            self.module = __import__(
                self.package + '.setup', globals(), locals()).setup

        return self.module.recipe

    def is_present(self):
        """Is init file present in actual directory?"""
        return path.exists(self.filename)
