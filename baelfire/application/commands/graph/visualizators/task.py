from .chooser import VisualizatorChooser
from .dependency import DependencyVisualizatorChooser
from .link import LinkVisualizatorChooser


class TaskVisualization(object):
    PREFIX = '\t'

    class Configure(object):
        dependency = DependencyVisualizatorChooser
        link = LinkVisualizatorChooser

    class Templates(object):
        task = '"%(url)s"[label="%(name)s",fillcolor=%(fill)s,style=filled];\n'
        always_run = '"%(url)s"[label="%(name)s",fillcolor=%(fill)s,style=filled,shape=octagon];\n'

    def __init__(self, url, report):
        self.url = url
        self.report = report

    def task(self):
        if self.report['needtorun']:
            if self.report['success']:
                fill = 'green'
            else:
                fill = 'red'
        else:
            fill = 'white'
        return {
            'url': self.url,
            'name': self.url.split('.')[-1],
            'fill': fill,
        }

    def render(self):
        self.rendered = ''
        self.render_task()
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

    def render_task(self):
        always_rebuild = 'baelfire.dependencies.dependency.AlwaysRebuild'
        if always_rebuild in self.report['dependencies']:
            self.rendered += (
                self.PREFIX + (self.Templates.always_run % self.task())
            )
        else:
            self.rendered += self.PREFIX + (self.Templates.task % self.task())


class TaskVisualizatorChooser(VisualizatorChooser):
    DEFAULT = TaskVisualization

    def generate_visualizators(self):
        pass
