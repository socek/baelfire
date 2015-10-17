from .chooser import VisualizatorChooser
from .dependency import DependencyVisualizatorChooser
from .link import LinkVisualizatorChooser


class TaskVisualization(object):
    PREFIX = '\t'
    TASK_TEMPLATE = '"%(url)s"[label="%(name)s"];\n'

    class Configure(object):
        dependency = DependencyVisualizatorChooser
        link = LinkVisualizatorChooser

    def __init__(self, url, report):
        self.url = url
        self.report = report

    def task(self):
        return {
            'url': self.url,
            'name': self.url.split('.')[-1],
        }

    def render(self):
        self.rendered = ''
        self.rendered += self.PREFIX + (self.TASK_TEMPLATE % self.task())
        for url, dependency in self.report['dependencies'].items():
            vdependency = self.Configure.dependency().choose(
                url,
                dependency,
            )
            vlink = self.Configure.link().choose(
                self.url,
                self.report,
                url,
                dependency,
            )
            self.rendered += vdependency.render()
            self.rendered += vlink.render()

        return self.rendered


class TaskVisualizatorChooser(VisualizatorChooser):
    DEFAULT = TaskVisualization

    def generate_visualizators(self):
        pass
