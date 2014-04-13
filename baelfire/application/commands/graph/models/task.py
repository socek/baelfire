from .visualization import Visualization
from.dependency import dependency_visualization


class TaskVisualization(Visualization):

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
        if self.is_always_rebuilding():
            return 'circle'
        else:
            return 'box'

    def details_data(self):
        return {
            'color': self.color(),
            'shape': self.shape(),
            'path': self.path(),
            'name': self.name(),
        }

    def dependencys(self):
        for dependency in self.data['dependencys']:
            cls = dependency_visualization(dependency['name'])
            yield cls(dependency, self)

    def is_always_rebuilding(self):
        names = [dependency['name']
                 for dependency in self.data['dependencys']]
        return 'AlwaysRebuild' in names