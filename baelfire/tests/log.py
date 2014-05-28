from json import loads, dumps
from io import StringIO
from mock import MagicMock
from soktest import TestCase

from baelfire.log import TaskLogger, Logger

PREFIX = 'baelfire.log.'


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
            'dependencies': [],
            'path': task.get_path_dotted.return_value,
        }, self.log.tasks['myname'])

    def test_add_dependecy(self):
        """Should add dependency log to a task log."""
        task = MagicMock()
        task.name = 'myname'
        self.log.tasks[task.name] = {'dependencies': []}
        dependency = MagicMock()
        dependency.name = 'depname'

        self.log.add_dependecy(task, dependency, {'this': 'is data'})

        element = self.log.tasks['myname']['dependencies'][0]

        self.assertEqual({'name': 'depname', 'data': {'this': 'is data'}},
                         element)

    def test_save(self):
        """Should save json into the file."""
        iobuffer = StringIO()
        self.add_mock('builtins.open', return_value=iobuffer)
        self.add_mock_object(iobuffer, 'close')

        task = MagicMock()
        task.name = 'myname'
        task.get_path_dotted.return_value = '/mypath'
        self.log.add_task(task, {'this': 'is data'})

        self.log.save()

        saved_data = loads(self.mocks['open'].return_value.getvalue())

        self.assertEqual([self.log.tasks['myname']], saved_data)

    def test_save_when_no_data_were_logged(self):
        """Should do nothing."""
        iobuffer = StringIO()
        self.add_mock('builtins.open', return_value=iobuffer)
        self.add_mock_object(iobuffer, 'close')

        self.log.save()

        self.assertEqual(0, self.mocks['open'].call_count)

    def test_read_when_log_does_not_exists(self):
        """Should return empty list."""
        self.add_mock(PREFIX + 'os')
        self.mocks['os'].path.exists.return_value = False

        self.assertEqual([], TaskLogger.read())

    def test_read_when_log_exists(self):
        """Should return logged data."""
        self.add_mock(PREFIX + 'os')
        self.mocks['os'].path.exists.return_value = True

        data = {'data': 'logged'}
        iobuffer = StringIO(dumps(data))
        self.add_mock('builtins.open', return_value=iobuffer)

        self.assertEqual(data, TaskLogger.read())


class LoggerTest(TestCase):

    def setUp(self):
        super().setUp()
        self.log = Logger()
        self.add_mock_object(self.log, 'common_log')
        self.add_mock_object(self.log, 'task_log')

    def test_info(self):
        """Should use .info from common logger."""
        result = self.log.info('arg', kw=1)

        self.assertEqual(self.mocks['common_log'].info.return_value, result)
        self.mocks['common_log'].info.assert_called_once_with('arg', kw=1)

    def test_error(self):
        """Should use .error from common logger."""
        result = self.log.error('arg', kw=1)

        self.assertEqual(self.mocks['common_log'].error.return_value, result)
        self.mocks['common_log'].error.assert_called_once_with('arg', kw=1)

    def test_warning(self):
        """Should use .warning from common logger."""
        result = self.log.warning('arg', kw=1)

        self.assertEqual(self.mocks['common_log'].warning.return_value, result)
        self.mocks['common_log'].warning.assert_called_once_with('arg', kw=1)

    def test_debug(self):
        """Should use .debug from common logger."""
        result = self.log.debug('arg', kw=1)

        self.assertEqual(self.mocks['common_log'].debug.return_value, result)
        self.mocks['common_log'].debug.assert_called_once_with('arg', kw=1)

    def test_task(self):
        """Should use .info from task logger."""
        result = self.log.task('arg', kw=1)

        self.assertEqual(self.mocks['task_log'].info.return_value, result)
        self.mocks['task_log'].info.assert_called_once_with('arg', kw=1)
