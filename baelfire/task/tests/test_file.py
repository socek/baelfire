from tempfile import NamedTemporaryFile

from baelfire.task import FileTask
from os import unlink
from os.path import exists


class ExampleFileTask(FileTask):
    output_name = 'file'

    def phase_settings(self):
        self.paths.set('file', ['/tmp', 'file.txt'])

    def build(self):
        open(self.output, 'w').close()


class ExampleSecondFileTask(FileTask):

    def build(self):
        open(self.output, 'w').close()


class TestFileTask(object):

    def test_normal(self):
        """
        FileTask should rebuild when file does not exists.
        """
        task = ExampleFileTask()
        task.phase_init()
        task.phase_settings()
        try:
            unlink(task.output)
        except:
            pass

        task.run()

        assert exists(task.output)
        assert task.report == {
            'baelfire.task.tests.test_file.ExampleFileTask': {
                'dependencies': [
                    {
                        'builded': True,
                        'filename': '/tmp/file.txt',
                        'index': 0,
                        'phase_validation': True,
                        'should_build': True,
                        'success': True,
                        'name': 'baelfire.dependencies.file.FileDoesNotExists',
                    },
                ],
                'needtorun': True,
                'runned': True,
                'success': True,
            },
            'last_index': 1,
        }

        task.run()
        assert task.report == {
            'baelfire.task.tests.test_file.ExampleFileTask': {
                'dependencies': [
                    {
                        'builded': True,
                        'filename': '/tmp/file.txt',
                        'index': 0,
                        'phase_validation': True,
                        'should_build': False,
                        'success': True,
                        'name': 'baelfire.dependencies.file.FileDoesNotExists',
                    },
                ],
                'needtorun': False,
                'runned': False,
                'success': False,
            },
            'last_index': 1,
        }

    def test_raw_path(self):
        ExampleSecondFileTask.output = NamedTemporaryFile().name
        task = ExampleSecondFileTask()
        task.run()

        assert task.report == {
            'baelfire.task.tests.test_file.ExampleSecondFileTask': {
                'dependencies': [
                    {
                        'builded': True,
                        'filename': ExampleSecondFileTask.output,
                        'index': 0,
                        'phase_validation': True,
                        'should_build': True,
                        'success': True,
                        'name': 'baelfire.dependencies.file.FileDoesNotExists',
                    },
                ],
                'needtorun': True,
                'runned': True,
                'success': True,
            },
            'last_index': 1,
        }
