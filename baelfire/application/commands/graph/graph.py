from subprocess import Popen
from yaml import load

from .visualizators import TaskVisualizatorChooser


class Graph(object):

    class Config(object):
        dot_path = 'graph.dot'
        png_path = 'graph.png'
        task = TaskVisualizatorChooser

    def __init__(self, path):
        self.path = path

    def read_report(self):
        file = open(self.path, 'r')
        return load(file)

    def render(self):
        self.generate_dot_file()
        self.generate_png_file()

    def generate_dot_file(self):
        self.report = self.read_report()
        with open(self.Config.dot_path, 'w') as stream:
            stream.write('digraph {\n')
            for key, element in sorted(self.report.items()):
                if type(element) is dict:
                    visualization = self.Config.task().choose(key, element)
                    stream.write(visualization.render())
            stream.write('}\n')

    def generate_png_file(self):
        spp = Popen(
            [
                'dot -Tpng %s -o %s' % (
                    self.Config.dot_path,
                    self.Config.png_path,
                )
            ],
            shell=True,
        )
        spp.wait()
