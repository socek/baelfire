from .dependency import get_dependency
from .link import get_link


class TaskVisualization(object):
    PREFIX = '\t'
    TASK_TEMPLATE = '"%(url)s"[label="%(name)s"];\n'

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
            vdependency = get_dependency(
                url,
                dependency,
            )
            vlink = get_link(
                self.url,
                self.report,
                url,
                dependency,
            )
            self.rendered += vdependency.render()
            self.rendered += vlink.render()

        return self.rendered


def get_task(url, report):
    return TaskVisualization(url, report)
