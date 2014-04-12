from tempfile import TemporaryFile
from subprocess import Popen

from baelfire.log import TaskLogger
from .task import TaskVisualization


class Graph(object):

    filename = '.baelfire.lastlog.png'

    def __init__(self):
        self.datalog = None

    def open(self):
        self.datalog = TemporaryFile()
        self.datalog.write(b'digraph {\n')

    def close(self):
        self.datalog.write(b'}\n')

    def open_lastlog(self):
        self.lastlog = TaskLogger.read()

    def generate_png(self):
        self.datalog.seek(0)
        filepipe = open(self.filename, 'w')
        spp = Popen(['dot', '-x', '-Tpng'],
                    stdin=self.datalog, stdout=filepipe)
        spp.wait()

    def write(self, data):
        self.datalog.write(data.encode('utf-8'))

    def __call__(self):
        self.open()
        self.open_lastlog()

        for task in self.lastlog:
            visualization = TaskVisualization(task)
            self.write(visualization.details())

            for dependency in visualization.dependencys():
                self.write(dependency.details())

        self.close()
        self.generate_png()
