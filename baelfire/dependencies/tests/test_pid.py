import os

from ..pid import PidFileIsRunning, PidFileIsNotRunning
from soktest import TestCase


PREFIX = 'baelfire.dependencies.pid.'


class PidFileIsRunningTest(TestCase):

    def setUp(self):
        super().setUp()
        self.dependency = PidFileIsRunning('/tmp/pidfile')

    def test_init(self):
        """Should set path and _pid"""
        self.assertEqual('/tmp/pidfile', self.dependency.path)

    def test_get_pid(self):
        """Should read pidfile and return its pid number"""
        pidfile = open('/tmp/pidfile', 'w')
        pidfile.write('1234')
        pidfile.close()

        self.assertEqual(1234, self.dependency.get_pid())

        os.unlink('/tmp/pidfile')

    def test_is_running_when_running(self):
        """Should return True if os.kill did not raise OSError"""
        self.add_mock(PREFIX + 'os')
        self.add_mock_object(self.dependency, 'get_pid', return_value=123)

        self.assertEqual(True, self.dependency.is_running())
        self.mocks['os'].kill.assert_called_once_with(123, 0)

    def test_is_running_when_not_running(self):
        """Should return False if os.kill did raise OSError"""
        self.add_mock(PREFIX + 'os')
        self.mocks['os'].kill.side_effect = OSError()
        self.add_mock_object(self.dependency, 'get_pid', return_value=123)

        self.assertEqual(False, self.dependency.is_running())
        self.mocks['os'].kill.assert_called_once_with(123, 0)

    def test_make(self):
        """Should return whatever is_running returns."""
        self.add_mock_object(self.dependency, 'is_running', return_value=123)

        self.assertEqual(123, self.dependency.make())


class PidFileIsNotRunningTest(TestCase):

    def setUp(self):
        super().setUp()
        self.dependency = PidFileIsNotRunning('/tmp/pidfile')

    def test_make(self):
        """Should return negative of whatever us_running returns."""
        self.add_mock_object(self.dependency, 'is_running', return_value=True)

        self.assertEqual(False, self.dependency.make())
