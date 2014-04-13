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
        self.assertEqual('box', self.visualization.shape())

    def test_details_data(self):
        """Should return data generated from object methods."""
        self.data['path'] = '/mypath'
        self.data['name'] = 'myname'
        self.data['data']['success'] = None
        self.data['data']['force'] = False
        self.data['data']['needed'] = False
        self.add_mock_object(self.visualization,
                             'is_always_rebuilding',
                             return_value=False)

        self.assertEqual({
            'path': '/mypath',
            'name': 'myname',
            'color': 'grey',
            'shape': 'box',
        }, self.visualization.details_data())

    def test_dependencys(self):
        """Should yield visualization of every dependency."""
        self.data['dependencys'] = [{'name': 'one'}]
        self.add_mock(PREFIX + 'dependency_visualization')

        data = list(self.visualization.dependencys())

        self.mocks['dependency_visualization'].assert_called_once_with('one')
        cls = self.mocks['dependency_visualization'].return_value
        cls.assert_called_once_with({'name': 'one'}, self.visualization)
        self.assertEqual([cls.return_value], data)

    def test_is_always_rebuilding_when_alwaysrebuild_in_depenencys(self):
        """Should return true."""
        self.data['dependencys'] = [{'name': "AlwaysRebuild"}]

        self.assertEqual(True, self.visualization.is_always_rebuilding())
