from .chooser import VisualizatorChooser


class DependencyVisualization(object):
    PREFIX = '\t\t'
    DEPENDENCY_TEMPLATE = '"%(url)s"[label="%(name)s",fillcolor=%(fill)s,shape=diamond,style=filled];\n'

    def __init__(self, url, report):
        self.url = url
        self.report = report

    def dependency(self):
        if self.report['should_build']:
            if self.report['success']:
                fill = 'yellow'
            else:
                fill = 'white'
        else:
            fill = 'white'
        return {
            'url': self.url,
            'name': self.url.split('.')[-1],
            'fill': fill,
        }

    def render(self):
        return self.PREFIX + self.DEPENDENCY_TEMPLATE % self.dependency()


class HiddenVisualization(DependencyVisualization):

    def render(self):
        return ''


class DependencyVisualizatorChooser(VisualizatorChooser):
    DEFAULT = DependencyVisualization

    def generate_visualizators(self):
        self.add_visualizator(
            'baelfire.dependencies.dependency.AlwaysRebuild',
            HiddenVisualization,
        )
        self.add_visualizator(
            'baelfire.dependencies.task.TaskDependency',
            HiddenVisualization,
        )
