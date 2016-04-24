from morfdict import PathDict
from morfdict import StringDict


class Core(object):

    def init(self):
        self.settings = StringDict()
        self.paths = PathDict()
        self.report = {'last_index': 0}

        self.paths['settings'] = self.settings

    def before_dependencies(self):
        pass

    def after_dependencies(self):
        pass
