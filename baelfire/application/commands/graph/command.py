from ..command import TriggeredCommand
from .models.graph import Graph


class GraphCommand(TriggeredCommand):

    def __init__(self):
        super().__init__('-g',
                         '--graph',
                         help='Generate graph from last runned command.')

    def make(self):
        Graph()()
