from morfdict import Paths
from morfdict import StringDict


class Core(object):

    def init(self):
        self.settings = StringDict()
        self.paths = Paths()
        self.report = {'last_index': 0}

    def before_dependencies(self):
        pass

    def after_dependencies(self):
        pass
