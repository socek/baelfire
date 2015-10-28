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
        for dependency in self.report['dependencies']:
            vdependency = self.Configure.dependency().choose(
                dependency['name'],
                dependency,
                self,
            )
            vlink = self.Configure.link().choose(
                self.url,
                self.report,
                vdependency.full_url,
                dependency,
            )
            self.rendered += vdependency.render()
            self.rendered += vlink.render()

        return self.rendered

    def render_task(self):
        always_rebuild = 'baelfire.dependencies.dependency.AlwaysRebuild'
        if always_rebuild in self.get_dependencies_names():
            self.rendered += (
                self.PREFIX + (self.Templates.always_run % self.task())
            )
        else:
            self.rendered += self.PREFIX + (self.Templates.task % self.task())

    def get_dependencies_names(self):
        return [item['name'] for item in self.report['dependencies']]


class TaskVisualizatorChooser(VisualizatorChooser):
    DEFAULT = TaskVisualization

    def generate_visualizators(self):
        pass
