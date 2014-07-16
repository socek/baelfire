from soktest import TestCase

from ..visualization import Visualization


class ExampleVisualization(Visualization):

    def details_data(self):
        return self.data


class VisualizationTest(TestCase):

    def setUp(self):
        super().setUp()
        self.data = {}
        self.visualization = ExampleVisualization(self.data)

    def test_init(self):
        self.assertEqual(self.data, self.visualization.data)

    def test_details(self):
        """Should return template filled up with .data"""
        self.data['path'] = '/path'
        self.data['name'] = 'name'
        self.data['shape'] = 'shape'
        self.data['color'] = 'color'
        self.assertEqual(
            '"/path" [label="name",shape=shape,regular=1,' +
            'style=filled,fillcolor=color];\n',
            self.visualization.details())
