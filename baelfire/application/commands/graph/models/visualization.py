class Visualization(object):
    template = '"%(path)s" [label="%(name)s",shape=%(shape)s,regular=1,' +\
        'style=filled,fillcolor=%(color)s];\n'

    def __init__(self, data):
        self.data = data

    def details(self):
        return self.template % self.details_data()
