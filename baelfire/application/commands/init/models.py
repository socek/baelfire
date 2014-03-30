import json
from os import path
from importlib import import_module
from subprocess import Popen

from baelfire.error import RecipeNotFoundError


class InitFile(object):

    filename = '.bael.init'

    def __init__(self):
        self.package_url = None
        self.setup_path = None
        self.recipe = None

    def assign(self, package_url, setup_path):
        self.package_url = package_url
        self.setup_path = setup_path

    def to_dict(self):
        return {
            'setup_path': self.setup_path,
            'package_url': self.package_url,
        }

    def from_dict(self, data):
        self.package_url = data['package_url']
        self.setup_path = data['setup_path']

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
        if self.recipe is None:
            url = self.package_url.split(':')
            module = import_module(url[0])
            try:
                self.recipe = getattr(module, url[1])
            except AttributeError:
                raise RecipeNotFoundError()
        return self.recipe

    def is_reinstall_needed(self):
        return not path.exists(self.filename) or \
            path.getmtime(self.filename) < path.getmtime(self.setup_path)

    def install_dependencys(self):
        if self.is_reinstall_needed():
            spp = Popen(['python', self.setup_path, 'test'])
            spp.wait()
            self.save()

    def is_present(self):
        """Is init file present in actual directory?"""
        return path.exists(self.filename)
