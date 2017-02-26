from io import BytesIO
from mock import MagicMock
from mock import patch
from pytest import mark
from pytest import yield_fixture
from subprocess import PIPE

from baelfire.dependencies.screen import ScreenIsNotRunning


class TestScreenIsNotRunning(object):
    DATA_NO_SCREENS = b'''No Sockets found in /run/screens/S-socek.

'''
    DATA_SCREEN = b'''There is a screen on:
        14709.pts-4.gringo      (Attached)
        18963.elo       (Detached)
2 Sockets in /run/screens/S-socek.
'''

    @yield_fixture
    def mlist_screens(self):
        with patch.object(ScreenIsNotRunning, '_list_screen') as mock:
            yield mock

    @yield_fixture
    def mpopen(self):
        with patch('baelfire.dependencies.screen.Popen') as mock:
            yield mock

    def test_get_screens_when_no_screens(self, mlist_screens):
        mlist_screens.return_value = BytesIO(self.DATA_NO_SCREENS)
        dep = ScreenIsNotRunning(None)
        assert list(dep.get_screens()) == []

    def test_get_screens(self, mlist_screens):
        mlist_screens.return_value = BytesIO(self.DATA_SCREEN)
        dep = ScreenIsNotRunning(None)
        assert list(dep.get_screens()) == [
            {'name': 'pts-4.gringo', 'pid': 14709, 'status': 'Attached'},
            {'name': 'elo', 'pid': 18963, 'status': 'Detached'}]

    @mark.parametrize(
        "name, parent_name, expected",
        [
            ('name', 'parent_name', 'name'),
            (None, 'parent_name', 'parent_name')
        ]
    )
    def test_screen_name(self, name, parent_name, expected):
        parent = MagicMock()
        parent.screen_name = parent_name
        dep = ScreenIsNotRunning(name)
        dep.set_parent(parent)

        assert dep.screen_name == expected

    @mark.parametrize(
        'screen_name, expected',
        [
            ('elo', False),
            ('else', True),
        ]
    )
    def test_should_build(self, mlist_screens, screen_name, expected):
        mlist_screens.return_value = BytesIO(self.DATA_SCREEN)
        dep = ScreenIsNotRunning(screen_name)
        assert dep.should_build() == expected

    def test_list_screen(self, mpopen):
        parent = MagicMock()
        parent.paths.get.return_value = '/usr/bin/screen'
        dep = ScreenIsNotRunning(None)
        dep.set_parent(parent)

        assert dep._list_screen() == mpopen.return_value.stdout
        mpopen.assert_called_once_with(
            ['/usr/bin/screen -list'],
            shell=True,
            stdout=PIPE)
        mpopen.return_value.wait.assert_called_once_with()
