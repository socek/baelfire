from .chooser import VisualizatorChooser


class DependencyVisualization(object):
    PREFIX = '\t\t'
    DEPENDENCY_TEMPLATE = '"%(url)s"[label="%(name)s"];\n'

    def __init__(self, url, report):
        self.url = url
        self.report = report

    def dependency(self):
        return {
            'url': self.url,
            'name': self.url.split('.')[-1],
        }

    def render(self):
        return self.PREFIX + self.DEPENDENCY_TEMPLATE % self.dependency()


class AlwaysRebuildVisualization(DependencyVisualization):
    DEPENDENCY_TEMPLATE = '"%(url)s"[label="%(name)s",shape=diamond];\n'


class HiddenVisualization(DependencyVisualization):

    def render(self):
        return ''


class DependencyVisualizatorChooser(VisualizatorChooser):
    DEFAULT = DependencyVisualization

    def generate_visualizators(self):
        self.add_visualizator(
            'baelfire.dependencies.dependency.AlwaysRebuild',
            AlwaysRebuildVisualization,
        )
        self.add_visualizator(
            'baelfire.dependencies.task.TaskDependency',
            HiddenVisualization,
        )
