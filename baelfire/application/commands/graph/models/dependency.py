from .visualization import Visualization


class DependencyVisualization(Visualization):
    connection_template = '"%(right)s" -> "%(left)s" [color="%(color)s"];\n'

    def __init__(self, data, parent):
        super().__init__(data)
        self.parent = parent

    def name(self):
        return self.data['name']

    def link_name(self):
        return self.data['name']

    def path(self):
        return '/'.join([self.parent.path(), self.data['name']])

    def is_link(self):
        return 'parent' in self.data['data']

    def right_path(self):
        if self.is_link():
            return self.data['data']['parent']['path']
        else:
            return self.path()

    def color(self):
        if self.data['data']['result']:
            return 'green'
        else:
            return 'brown'

    def shape(self):
        return 'triangle'

    def details_data(self):
        return {
            'color': self.color(),
            'shape': self.shape(),
            'name': self.name(),
            'path': self.path(),
        }

    def connection_details(self):
        return {
            'left': self.parent.path(),
            'right': self.right_path(),
            'name': self.link_name(),
            'color': self.color(),
        }

    def connection(self):
        return self.connection_template % self.connection_details()

    def details(self):
        data = ''
        if not self.is_link():
            data = super().details()
        data += self.connection()
        return data


class AlwaysRebuildVisualization(DependencyVisualization):

    def details(self):
        return ''


class FileDependencyVisualization(DependencyVisualization):

    def shape(self):
        return 'folder'

    def name(self):
        return self.data['data']['filenames'][0].replace('/', '\n/')

    def path(self):
        return '/%s?filename=%s' % (
            self.data['name'],
            self.data['data']['filenames'][0],
        )

transform = {
    'AlwaysRebuild': AlwaysRebuildVisualization,
    'FileChanged': FileDependencyVisualization,
    'FileDoesNotExists': FileDependencyVisualization,
}


def dependency_visualization(name):
    return transform.get(name, DependencyVisualization)
