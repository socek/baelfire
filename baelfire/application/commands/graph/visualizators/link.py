from .chooser import VisualizatorChooser


class LinkVisualization(object):
    PREFIX = '\t\t\t'
    LINK_TEMPLATE = '"%(right_url)s" -> "%(left_url)s";\n'
    HIDDEN_RIGHTS = [
        'baelfire.dependencies.dependency.AlwaysRebuild',
    ]

    def __init__(self, left_url, left, right_url, right):
        self.left_url = left_url
        self.left = left
        self.right_url = right_url
        self.right = right

    def link(self):
        task = self.right.get('task')
        if task:
            right_url = task
        else:
            right_url = self.right_url

        return {
            'left_url': self.left_url,
            'right_url': right_url,
        }

    def render(self):
        if self.right['name'] in self.HIDDEN_RIGHTS:
            return ''
        return self.PREFIX + (self.LINK_TEMPLATE % self.link())


class LinkVisualizatorChooser(VisualizatorChooser):
    DEFAULT = LinkVisualization

    def generate_visualizators(self):
        pass
