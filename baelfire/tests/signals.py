from mock import MagicMock
from soktest import TestCase

from ..signals import SignalHandling

PREFIX = 'baelfire.signals.'


class SignalHandlingTest(TestCase):

    def setUp(self):
        super().setUp()
        self.recipe = MagicMock()
        self.add_mock(PREFIX + 'signal')
        self.handler = SignalHandling(self.recipe)

    def test_init(self):
        self.assertEqual(self.recipe, self.handler.recipe)
        self.assertEqual(6, self.mocks['signal'].signal.call_count)

    def test_send_signal(self):
        """Should send signall to subproccess."""
        spp = MagicMock()
        spp.poll.return_value = None

        self.handler.send_signal(spp, 'signal')

        spp.poll.assert_called_once_with()
        spp.send_signal.assert_called_once_with('signal')

    def test_send_signal_on_oserror(self):
        """Should silent OSError."""
        spp = MagicMock()
        spp.poll.return_value = None
        spp.send_signal.side_effect = OSError()

        self.handler.send_signal(spp, 'signal')

        spp.poll.assert_called_once_with()
        spp.send_signal.assert_called_once_with('signal')

    def test_send_signal_when_subprocess_ended(self):
        """Should do nothing when subprocess is ended."""
        spp = MagicMock()
        spp.poll.return_value = 0

        self.handler.send_signal(spp, 'signal')

        spp.poll.assert_called_once_with()
        self.assertEqual(0, spp.send_signal.call_count)

    def test_on_signal(self):
        """Should set recipe flag aborting."""
        self.recipe._spp = None

        self.handler.on_signal('signum', 'frame')

        self.assertEqual(True, self.recipe.aborting)

    def test_on_signal_with_subprocess(self):
        """Should send signum to subprocess"""
        self.recipe._spp.poll.return_value = None

        self.handler.on_signal('signum', 'frame')

        self.assertEqual(True, self.recipe.aborting)
        self.recipe._spp.poll.assert_called_once_with()
        self.recipe._spp.send_signal.assert_called_once_with('signum')
