from subprocess import PIPE

from mock import MagicMock
from soktest import TestCase

from ..error import CommandError, CommandAborted
from ..process import Process

PREFIX = 'baelfire.process.'


class ProcessTest(TestCase):

    def setUp(self):
        super().setUp()
        self.task = MagicMock()
        self.recipe = self.task.recipe
        self.process = Process(self.task)

    def test_init(self):
        self.assertEqual(self.task, self.process.task)
        self.assertEqual(self.task.recipe, self.process.recipe)
        self.assertEqual(None, self.process.spp)

    def test_prepare_args(self):
        """Should set default values for args and kwargs."""
        data = {'stdout': 'something', 'stderr': 's2'}
        self.process.prepare_args([], data)

        self.assertEqual(
            {'stdout': 'something', 'shell': True, 'stderr': 's2'}, data)

    def test_pipes(self):
        """Should return pipes ready to read."""
        self.add_mock(PREFIX + 'select')
        self.mocks['select'].return_value = ('one', 'two', 'three')
        self.process.spp = MagicMock()

        result = self.process.pipes()

        self.assertEqual('one', result)
        self.mocks['select'].assert_called_once_with(
            [
                self.process.spp.stdout,
                self.process.spp.stderr],
            [],
            [])

    def test_pipes_on_InterruptedError(self):
        """Should raise CommandAborted on InterruptedError."""
        self.add_mock(PREFIX + 'select')
        self.mocks['select'].side_effect = InterruptedError()
        self.process.spp = MagicMock()

        self.assertRaises(CommandAborted, self.process.pipes)

    def test_write_to_log_no_read_avalible(self):
        """Should do nothing when pipe is not in ._pipes"""
        self.process.spp = MagicMock()
        self.process._pipes = []

        self.process.write_to_log('pipe', 'loglevel')

        self.assertEqual(0, self.recipe.log.process_log.pipe.call_count)

    def test_write_to_log_when_read_avalible(self):
        """Should write to a log what was read from pipes."""
        self.process.spp = MagicMock()
        log = self.recipe.log.process_log.loglevel
        pipe = self.process.spp.pipe
        self.process._pipes = [pipe]

        self.process.write_to_log('pipe', 'loglevel')
        pipe.readline.assert_called_once_with()
        pipe.readline.return_value.decode.assert_called_once_with('utf-8')
        data = pipe.readline.return_value.decode.return_value
        data.strip.assert_called_once_with()
        log.assert_called_once_with(
            data.strip.return_value)

    def test_post_run_when_aborting(self):
        """Should raise CommandAborted when recipe is set to aborting state."""
        self.recipe.aborting = True

        self.assertRaises(CommandAborted, self.process.post_run)

    def test_post_run_when_process_returne_error(self):
        """Should raise CommandError when process exited with error."""
        self.process.spp = MagicMock()
        self.process.spp.returncode = 1

        self.assertRaises(CommandError, self.process.post_run)

    def test_post_run_all_ok(self):
        """Should do nothing when process exited with success."""
        self.process.spp = MagicMock()
        self.process.spp.returncode = 0

        self.assertEqual(None, self.process.post_run())

    def test_call(self):
        self.add_mock(PREFIX + 'Popen')
        self.mocks['Popen'].return_value.returncode = 0

        self.process()

        self.mocks['Popen'].assert_called_once_with(shell=True)
