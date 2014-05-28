from soktest import TestCase

from ..task import TaskVisualization

PREFIX = 'baelfire.application.commands.graph.models.task.'


class TaskVisualizationTest(TestCase):

    def setUp(self):
        super().setUp()
        self.data = {'data': {}}
        self.visualization = TaskVisualization(self.data)

    def test_name(self):
        """Should return data['name']"""
        self.data['name'] = 'myname'
        self.assertEqual('myname', self.visualization.name())

    def test_path(self):
        """Should return data['path']"""
        self.data['path'] = 'mypath'
        self.assertEqual('mypath', self.visualization.path())

    def test_color_on_fail(self):
        """Should return red when task has filed."""
        self.data['data']['success'] = False
        self.assertEqual('red', self.visualization.color())

    def test_color_on_force(self):
        """Should return yellow when task had been forced to run."""
        self.data['data']['success'] = True
        self.data['data']['force'] = True
        self.assertEqual('yellow', self.visualization.color())

    def test_color_on_needed(self):
        """Should return green, when task was invoked by dependency."""
        self.data['data']['success'] = True
        self.data['data']['force'] = False
        self.data['data']['needed'] = True

        self.assertEqual('green', self.visualization.color())

    def test_color_when_task_has_not_been_run(self):
        """Should return grey."""
        self.data['data']['success'] = None
        self.data['data']['force'] = False
        self.data['data']['needed'] = False

        self.assertEqual('grey', self.visualization.color())

    def test_shape_when_alwaysrebuild_depencency_present(self):
        """Should return circle."""
        self.add_mock_object(self.visualization,
                             'is_always_rebuilding',
                             return_value=True)
        self.assertEqual('circle', self.visualization.shape())

    def test_shape_without_alwaysrebuild(self):
        """Should return box"""
        self.add_mock_object(self.visualization,
                             'is_always_rebuilding',
                             return_value=False)
        self.visualization.data['dependencies'] = [1]
        self.assertEqual('box', self.visualization.shape())

    def test_shape_when_empty_dependency_list(self):
        """Should return hexagon when task has no dependency and not
        output_file setted."""
        self.add_mock_object(self.visualization,
                             'is_always_rebuilding',
                             return_value=False)
        self.visualization.data['dependencies'] = []
        self.visualization.data['data']['output_file'] = None
        self.assertEqual('hexagon', self.visualization.shape())

    def test_details_data(self):
        """Should return data generated from object methods."""
        self.data['path'] = '/mypath'
        self.data['name'] = 'myname'
        self.data['data']['success'] = None
        self.data['data']['force'] = False
        self.data['data']['needed'] = False
        self.data['dependencies'] = [1]
        self.add_mock_object(self.visualization,
                             'is_always_rebuilding',
                             return_value=False)

        self.assertEqual({
            'path': '/mypath',
            'name': 'myname',
            'color': 'grey',
            'shape': 'box',
        }, self.visualization.details_data())

    def test_dependencies(self):
        """Should yield visualization of every dependency."""
        self.data['dependencies'] = [{'name': 'one'}]
        self.add_mock(PREFIX + 'dependency_visualization')

        data = list(self.visualization.dependencies())

        self.mocks['dependency_visualization'].assert_called_once_with('one')
        cls = self.mocks['dependency_visualization'].return_value
        cls.assert_called_once_with({'name': 'one'}, self.visualization)
        self.assertEqual([cls.return_value], data)

    def test_is_always_rebuilding_when_alwaysrebuild_in_depenencys(self):
        """Should return true."""
        self.data['dependencies'] = [{'name': "AlwaysRebuild"}]

        self.assertEqual(True, self.visualization.is_always_rebuilding())

    def test_link_data(self):
        """Should return data generated from object methods."""
        self.data['path'] = '/mypath'
        data = self.visualization.link_data('mylink')
        self.assertEqual({
            'left': '/mypath',
            'right': 'mylink',
        }, data)

    def test_links(self):
        """Should return filled up templates."""
        self.data['path'] = '/mypath'
        self.data['data'] = {
            'links': ['/mylink'],
        }
        data = self.visualization.links()

        self.assertEqual('"/mylink" -> "/mypath" [style=dashed];\n', data)

    def test_invoked(self):
        """invoked should return filled up templates."""
        self.data['path'] = '/mypath'
        self.data['data'] = {
            'invoked': ['/myinvoked'],
        }

        expected = '"/myinvoked" -> "/mypath" [style=dotted];\n'
        self.assertEqual(expected, self.visualization.invoked())
