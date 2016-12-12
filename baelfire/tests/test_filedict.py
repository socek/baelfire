from tempfile import NamedTemporaryFile

from mock import patch
from pytest import raises

from ..filedict import FileDict


class TestFileDict(object):

    @property
    def path(self):
        return NamedTemporaryFile().name

    def obj(self):
        return FileDict(self.path)

    def test_saving(self):
        data = self.obj()
        data['first'] = 10
        data['second'] = 'xxx'
        data.save()

        loader = FileDict(data.path)
        loader.load()

        assert dict(data) == dict(loader)

    def test_loading(self):
        data = self.obj()
        data['first'] = 10
        data['second'] = 'xxx'
        data.save()

        data['third'] = 'lel'
        data.load()

        assert dict(data) == {
            'first': 10,
            'second': 'xxx',
        }

    def test_loading_on_error(self):
        data = self.obj()
        with raises(IOError):
            data.load()
        assert dict(data) == {}

    def test_loading_with_ignore_error(self):
        assert dict(self.obj().load(True)) == {}

    def test_ensure_key_not_exists(self):
        obj = self.obj()
        patcher = patch.object(obj, 'read_from_stdin')

        with patcher as mock:
            obj.ensure_key_exists('key', 'description')
            mock.assert_called_once_with('key', 'description')

    def test_ensure_key_exists(self):
        obj = self.obj()
        patcher = patch.object(obj, 'read_from_stdin')
        obj['key'] = 'x'

        with patcher as mock:
            obj.ensure_key_exists('key', 'description')
            assert mock.called is False

    def test_read_from_stdin(self):
        obj = self.obj()
        patcher = patch('baelfire.filedict.input')

        with patcher as mock:
            obj.read_from_stdin('key', 'description')
            mock.assert_called_once_with('description: ')
            assert obj['key'] == mock.return_value

    def test_read_from_stdin_without_description(self):
        obj = self.obj()
        patcher = patch('baelfire.filedict.input')

        with patcher as mock:
            obj.read_from_stdin('key')
            mock.assert_called_once_with('')
            assert obj['key'] == mock.return_value
