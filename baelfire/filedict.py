from yaml import dump
from yaml import load
from os.path import exists


class FileDict(dict):

    def __init__(self, path):
        self.path = path

    def load(self, ignore_errors=False):
        self.clear()
        if ignore_errors and not self.exists():
            return self
        with open(self.path, 'r') as file:
            self.update(load(file))
        return self

    def exists(self):
        return exists(self.path)

    def save(self):
        with open(self.path, 'w') as file:
            dump(dict(self), file, default_flow_style=False)

    def ensure_key_exists(self, key, description=''):
        if key not in self:
            self.read_from_stdin(key, description)

    def read_from_stdin(self, key, description=''):
        if description:
            description += ': '
        self[key] = input(description)
