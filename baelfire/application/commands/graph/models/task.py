from .visualization import Visualization
from.dependency import dependency_visualization


class TaskVisualization(Visualization):

    link_template = '"%(right)s" -> "%(left)s" [style=dashed];\n'
    invoked_template = '"%(right)s" -> "%(left)s" [style=dotted];\n'

    def name(self):
        return self.data['name']

    def path(self):
        return self.data['path']

    def color(self):
        data = self.data['data']
        if data['success'] is False:
            return 'red'

        if data['force']:
            return 'yellow'
        if data['needed']:
            return 'green'
        return 'grey'

    def shape(self):
        def has_no_dependencies():
            return len(self.data['dependencies']) == 0 and \
                self.data['data']['output_file'] is None
        if self.is_always_rebuilding():
            return 'circle'
        elif has_no_dependencies():
            return 'hexagon'
        else:
            return 'box'

    def details_data(self):
        return {
            'color': self.color(),
            'shape': self.shape(),
            'path': self.path(),
            'name': self.name(),
        }

    def dependencies(self):
        for dependency in self.data['dependencies']:
            cls = dependency_visualization(dependency['name'])
            yield cls(dependency, self)

    def is_always_rebuilding(self):
        names = [dependency['name']
                 for dependency in self.data['dependencies']]
        return 'AlwaysRebuild' in names

    def link_data(self, link):
        return {
            'left': self.path(),
            'right': link,
        }

    def links(self):
        data = ''
        for link in self.data['data']['links']:
            data += self.link_template % self.link_data(link)
        return data

    def invoked(self):
        data = ''
        for path in self.data['data']['invoked']:
            data += self.invoked_template % self.invoked_data(path)
        return data

    def invoked_data(self, path):
        return {
            'left': self.path(),
            'right': path,
        }
