from yaml import load

from .visualizators import get_task


class Graph(object):

    GRAPH_PATH = 'graph.dot'
    get_task = get_task

    def __init__(self, path):
        self.path = path

    def read_report(self):
        file = open(self.path, 'r')
        return load(file)

    def render(self):
        self.report = self.read_report()
        with open(self.GRAPH_PATH, 'w') as stream:
            stream.write('digraph {\n')
            for key, element in self.report.items():
                if type(element) is dict:
                    visualization = self.get_task(key, element)
                    stream.write(visualization.render())
            stream.write('}\n')
