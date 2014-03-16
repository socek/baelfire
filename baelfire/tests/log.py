from json import loads
from io import StringIO
from mock import MagicMock
from soktest import TestCase

from baelfire.log import TaskLogger


class TaskLoggerTest(TestCase):

    def setUp(self):
        super().setUp()
        self.log = TaskLogger()

    def test_add_task(self):
        """Should add task to data log."""
        task = MagicMock()
        task.name = 'myname'
        self.log.add_task(task, {'this': 'is data'})

        self.assertEqual({
            'name': 'myname',
            'data': {'this': 'is data'},
            'dependencys': [],
        }, self.log.tasks['myname'])

    def test_add_dependecy(self):
        """Should add dependency log to a task log."""
        task = MagicMock()
        task.name = 'myname'
        self.log.tasks[task.name] = {'dependencys': []}
        dependency = MagicMock()
        dependency.name = 'depname'

        self.log.add_dependecy(task, dependency, {'this': 'is data'})

        element = self.log.tasks['myname']['dependencys'][0]

        self.assertEqual({'name': 'depname', 'data': {'this': 'is data'}},
                         element)

    def test_save(self):
        """Should save json into the file."""
        iobuffer = StringIO()
        self.add_mock('builtins.open', return_value=iobuffer)
        self.add_mock_object(iobuffer, 'close')

        task = MagicMock()
        task.name = 'myname'
        self.log.add_task(task, {'this': 'is data'})

        self.log.save()

        saved_data = loads(self.mocks['open'].return_value.getvalue())

        self.assertEqual([self.log.tasks['myname']], saved_data)
