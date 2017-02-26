from tempfile import NamedTemporaryFile
from time import sleep

from mock import MagicMock

from ..file import FileChanged
from ..file import FileDependency
from ..file import FileDoesNotExists
from ..file import FileExists


class TestFileDependency(object):

    def test_source(self):
        """
        FileDependency should accept source name wich will be later used as a
        key in .paths.
        """
        dependency = FileDependency('myname')
        parent = MagicMock()
        parent.paths = {'myname': 'success'}
        dependency.set_parent(parent)

        assert dependency.path == 'success'

    def test_phase_data(self):
        """
        FileDependency should add filename in report.
        """
        dependency = FileDependency('myname')
        parent = MagicMock()
        parent.paths = {'myname': 'success'}
        parent.myreport = {'dependencies': []}
        dependency.set_parent(parent)

        dependency.phase_data()

        assert dependency.myreport == {
            'filename': 'success',
            'name': 'baelfire.dependencies.file.FileDependency',
        }


class TestFileChanged(object):

    def test_on_output_not_existing(self):
        """
        FileChanged should indicate to rebuild if output file does not exists.
        """
        name = NamedTemporaryFile().name
        parent = MagicMock()
        parent.output = name
        dependency = FileChanged('tmp')
        dependency.set_parent(parent)

        assert dependency.should_build() is True

    def test_on_source_not_existing(self):
        """
        FileChanged should indicate to rebuild if source file does not exists.
        """
        name = NamedTemporaryFile(delete=False).name
        parent = MagicMock()
        parent.output = name
        dependency = FileChanged(raw_path=NamedTemporaryFile().name)
        dependency.set_parent(parent)

        assert dependency.should_build() is True

    def test_on_output_younger(self):
        """
        FileChanged should indicate to rebuild if output file is younger then
        the source file.
        """
        with NamedTemporaryFile(delete=False) as destination:
            destination.close()
            sleep(0.01)
            with NamedTemporaryFile(delete=False) as source:
                source.close()
                parent = MagicMock()
                parent.output = destination.name
                parent.paths = {
                    'source': source.name,
                }
                dependency = FileChanged('source')
                dependency.set_parent(parent)
                # import ipdb ; ipdb.set_trace()
                assert dependency.should_build() is True

    def test_on_output_older(self):
        """
        FileChanged should indicate not to rebuild if output file is older then
        the source file.
        """
        with NamedTemporaryFile(delete=False) as source:
            source.close()
            with NamedTemporaryFile(delete=False) as destination:
                destination.close()
                parent = MagicMock()
                parent.output = destination.name
                parent.paths = {
                    'source': source.name,
                }
                dependency = FileChanged('source')
                dependency.set_parent(parent)

                assert dependency.should_build() is False


class TestFileDoesNotExists(object):

    def test_on_file_not_exists(self):
        """
        FileDoesNotExists should indicate to rebuild if file is not existing.
        """
        name = NamedTemporaryFile().name
        parent = MagicMock()
        parent.paths = {
            'source': name,
        }
        dependency = FileDoesNotExists('source')
        dependency.set_parent(parent)

        assert dependency.should_build() is True

    def test_on_file_exists(self):
        """
        FileDoesNotExists should indicate not to rebuild if file exists.
        """
        with NamedTemporaryFile(delete=False) as source:
            parent = MagicMock()
            parent.paths = {
                'source': source.name,
            }
            dependency = FileDoesNotExists('source')
            dependency.set_parent(parent)

            assert dependency.should_build() is False


class TestFileExists(object):

    def test_on_file_not_exists(self):
        """
        FileExists should indicate not to rebuild if file is not existing.
        """
        name = NamedTemporaryFile().name
        parent = MagicMock()
        parent.paths = {
            'source': name,
        }
        dependency = FileExists('source')
        dependency.set_parent(parent)

        assert dependency.should_build() is False

    def test_on_file_exists(self):
        """
        FileExists should indicate to rebuild if file exists.
        """
        with NamedTemporaryFile(delete=False) as source:
            parent = MagicMock()
            parent.paths = {
                'source': source.name,
            }
            dependency = FileExists('source')
            dependency.set_parent(parent)

            assert dependency.should_build() is True
