from .chooser import VisualizatorChooser


class DependencyVisualization(object):
    PREFIX = '\t\t'
    DEPENDENCY_TEMPLATE = '"%(url)s"[label="%(name)s",fillcolor=%(fill)s,shape=box,style=filled];\n'

    def __init__(self, url, report, parent):
        self.parent = parent
        self.url = url
        self.report = report

    def dependency(self):
        return {
            'url': self.full_url,
            'name': self.get_name(),
            'fill': self.get_fill(),
        }

    def render(self):
        return self.PREFIX + self.DEPENDENCY_TEMPLATE % self.dependency()

    @property
    def full_url(self):
        return self.url + ':' + str(self.report['index'])

    def get_fill(self):
        if self.report['should_build']:
            if self.report['success']:
                return 'yellow'
            else:
                return 'white'
        return 'white'

    def get_name(self):
        return self.url.split('.')[-1]


class HiddenVisualization(DependencyVisualization):

    def render(self):
        return ''


class FileVisualization(DependencyVisualization):

    def get_name(self):
        return super(FileVisualization, self).get_name() + r'\n' + self.report['filename']


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
        ),
        self.add_visualizator(
            'baelfire.dependencies.task.RunBefore',
            HiddenVisualization,
        )
        self.add_visualizator(
            'baelfire.dependencies.file.FileDoesNotExists',
            FileVisualization,
        )
        self.add_visualizator(
            'baelfire.dependencies.file.FileChanged',
            FileVisualization,
        )
