from mock import MagicMock
from soktest import TestCase

from ..dependency import (DependencyVisualization,
                          AlwaysRebuildVisualization,
                          FileDependencyVisualization,
                          dependency_visualization)


class DependencyVisualizationTest(TestCase):

    def setUp(self):
        super().setUp()
        self.data = {}
        self.parent = MagicMock()
        self.visualization = DependencyVisualization(self.data, self.parent)

    def test_name(self):
        """Should return data['name']"""
        self.data['name'] = 'myname'
        self.assertEqual('myname', self.visualization.name())

    def test_link_name(self):
        """Should return data['name']"""
        self.data['name'] = 'myname'
        self.assertEqual('myname', self.visualization.link_name())

    def test_path(self):
        """Should return path with parent and dependency."""
        self.parent.path.return_value = '/parent'
        self.data['name'] = 'myname'

        self.assertEqual('/parent/myname', self.visualization.path())

    def test_is_link(self):
        """Should return true if dependency has a parent."""
        self.data['data'] = {'parent': {}}

        self.assertEqual(True, self.visualization.is_link())

    def test_right_path_when_is_link(self):
        """Should return parent path."""
        self.data['data'] = {'parent': {'path': '/mypath'}}

        self.assertEqual('/mypath', self.visualization.right_path())

    def test_right_path_when_not_a_link(self):
        """Should return .path()"""
        self.data['name'] = 'depname'
        self.data['data'] = {}
        self.parent.path.return_value = '/parent'

        self.assertEqual('/parent/depname', self.visualization.right_path())

    def test_color(self):
        """Should return brown on fail."""
        self.data['data'] = {'result': False}
        self.assertEqual('brown', self.visualization.color())

    def test_color_on_success(self):
        """Should return green on success."""
        self.data['data'] = {'result': True}
        self.assertEqual('green', self.visualization.color())

    def test_shape(self):
        """Should return circle."""

        self.assertEqual('triangle', self.visualization.shape())

    def test_details_data(self):
        """Should return data generated from object methods."""
        self.data['name'] = 'depname'
        self.data['data'] = {'result': True}
        self.parent.path.return_value = '/parent'

        self.assertEqual({
            'color': 'green',
            'shape': 'triangle',
            'name': 'depname',
            'path': '/parent/depname',
        }, self.visualization.details_data())

    def test_connection_details(self):
        """Should return data generated from object methods."""
        self.parent.path.return_value = '/1parentpath'
        self.data['data'] = {
            'parent': {'path': '/2parentpath'}, 'result': False}
        self.data['name'] = 'depname'

        data = self.visualization.connection_details()
        self.assertEqual({
            'left': '/1parentpath',
            'name': 'depname',
            'right': '/2parentpath',
            'color': 'brown'}, data)

    def test_connection(self):
        """Should return template filled up with .data"""
        self.parent.path.return_value = '/1parentpath'
        self.data['data'] = {
            'parent': {'path': '/2parentpath'}, 'result': False}
        self.data['name'] = 'depname'

        data = self.visualization.connection()

        self.assertEqual(
            '"/2parentpath" -> "/1parentpath" [color="brown"];\n', data)

    def test_details_when_not_a_link(self):
        """Should return template filled up with .data"""
        self.parent.path.return_value = '/1parentpath'
        self.data['data'] = {'result': False}
        self.data['name'] = 'depname'

        data = self.visualization.details()

        self.assertEqual(
            '''"/1parentpath/depname" [label="depname",shape=triangle,regular=1,style=filled,fillcolor=brown];
"/1parentpath/depname" -> "/1parentpath" [color="brown"];
''', data)

    def test_details_when_not_a_link_with_success(self):
        """Should return template filled up with .data"""
        self.parent.path.return_value = '/1parentpath'
        self.data['data'] = {'result': True}
        self.data['name'] = 'depname'

        data = self.visualization.details()

        self.assertEqual(
            '''"/1parentpath/depname" [label="depname",shape=triangle,regular=1,style=filled,fillcolor=green];
"/1parentpath/depname" -> "/1parentpath" [color="green"];
''', data)

    def test_details_when_is_a_link(self):
        """Should return template filled up with .data"""
        self.parent.path.return_value = '/1parentpath'
        self.data['data'] = {
            'parent': {'path': '/2parentpath'}, 'result': False}
        self.data['name'] = 'depname'

        data = self.visualization.details()

        self.assertEqual(
            '''"/2parentpath" -> "/1parentpath" [color="brown"];
''', data)


class AlwaysRebuildVisualizationTest(TestCase):

    def setUp(self):
        super().setUp()
        self.data = {}
        self.parent = MagicMock()
        self.visualization = AlwaysRebuildVisualization(self.data, self.parent)

    def test_details(self):
        """Should return empty string"""
        self.assertEqual('', self.visualization.details())


class FileDependencyVisualizationTest(TestCase):

    def setUp(self):
        super().setUp()
        self.data = {}
        self.parent = MagicMock()
        self.visualization = FileDependencyVisualization(
            self.data, self.parent)

    def test_name(self):
        """Should return first filename."""
        self.data['data'] = {'filenames': ['filename']}

        self.assertEqual('filename', self.visualization.name())

    def test_path(self):
        """Should return /(dependency name)?filename=(first filname)"""
        self.data['name'] = 'dependency_name'
        self.data['data'] = {'filenames': ['filename']}

        self.assertEqual(
            '/dependency_name?filename=filename', self.visualization.path())

    def test_shape(self):
        """Should return 'folder'."""
        self.assertEqual('folder', self.visualization.shape())


class DependencyVisualizationFunctionTest(TestCase):

    def test_when_element_in_transform(self):
        """Should return wanted class."""
        self.assertEqual(
            AlwaysRebuildVisualization,
            dependency_visualization('AlwaysRebuild'))

    def test_when_element_not_in_transform(self):
        """Should return default visualization: DependencyVisualization."""
        self.assertEqual(
            DependencyVisualization, dependency_visualization('something'))
