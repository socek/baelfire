class LinkVisualization(object):
    PREFIX = '\t\t\t'
    LINK_TEMPLATE = '"%(left_url)s" -> "%(right_url)s";\n'

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
        return self.PREFIX + (self.LINK_TEMPLATE % self.link())


def get_link(left_url, left, right_url, right):
    return LinkVisualization(left_url, left, right_url, right)
