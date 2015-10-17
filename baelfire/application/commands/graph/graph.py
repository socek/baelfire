from subprocess import Popen
from yaml import load

from .visualizators import get_task


class Graph(object):

    class Config(object):
        dot_path = 'graph.dot'
        png_path = 'graph.png'

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
            for key, element in self.report.items():
                if type(element) is dict:
                    visualization = self.get_task(key, element)
                    stream.write(visualization.render())
            stream.write('}\n')

    def get_task(self, key, element):
        return get_task(key, element)

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
