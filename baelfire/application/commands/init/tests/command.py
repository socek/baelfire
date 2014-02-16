import os
import json

from soktest import TestCase

from ..models import InitFile
from ..error import RecipePackageNotValidError
from ..command import Init

PREFIX = 'baelfire.application.commands.init.command.'


class InitTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = Init()

    def test_init(self):
        self.assertEqual('init', self.command.name)
        self.assertEqual(('-i', '--init'), self.command.args)
        self.assertEqual(
            {'dest': 'init', 'nargs': 1, 'help': 'Inits package.'},
            self.command.kwargs)

    def test_module_exists_dir(self):
        """Should return True if module exists as a directory."""
        def exists_side_effect(path):
            if path == '/tmp/__init__.py':
                return True
            else:
                return False

        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.side_effect = exists_side_effect
        self.mocks['path'].join.side_effect = os.path.join

        self.assertEqual(True, self.command.module_exists('/tmp'))

    def test_module_exists_py(self):
        """Should return True if module exists as a .py (or .pyc, or .pyo)
        file."""
        def exists_side_effect(path):
            if path == '/tmp.py':
                return True
            else:
                return False

        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.side_effect = exists_side_effect
        self.mocks['path'].join.side_effect = os.path.join

        self.assertEqual(True, self.command.module_exists('/tmp'))

    def test_module_exists_error(self):
        """Should return False if no module exists."""
        def exists_side_effect(path):
            return False

        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.side_effect = exists_side_effect
        self.mocks['path'].join.side_effect = os.path.join

        self.assertEqual(False, self.command.module_exists('/tmp'))

    def test_validate_package_success(self):
        """Should return None if no error found."""
        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.return_value = True
        self.add_mock(PREFIX + 'InitFile')

        self.assertEqual(None, self.command.validate_package('/tmp'))

    def test_validate_package_no_directory(self):
        """Should raise RecipePackageNotValidError when no directory found."""
        def exists_side_effect(path):
            if path == '/tmp':
                return False
            else:
                return True

        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.side_effect = exists_side_effect
        self.mocks['path'].join.side_effect = os.path.join

        self.assertRaises(
            RecipePackageNotValidError, self.command.validate_package, '/tmp')

    def test_validate_package_no_setup(self):
        """Should raise RecipePackageNotValidError when no setup.py found."""
        def exists_side_effect(path):
            if path in [
                    '/tmp/setup/__init__.py',
                    '/tmp/setup.py',
                    '/tmp/setup.pyc',
                    '/tmp/setup.pyo',
            ]:
                return False
            else:
                return True

        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.side_effect = exists_side_effect
        self.mocks['path'].join.side_effect = os.path.join

        self.assertRaises(
            RecipePackageNotValidError, self.command.validate_package, '/tmp')

    def test_validate_package_no_recipe(self):
        """Should raise RecipePackageNotValidError when no recipe var
        found in setup.py."""
        self.add_mock(PREFIX + 'InitFile')
        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.return_value = True
        self.mocks['path'].join.side_effect = os.path.join
        self.mocks['InitFile'].return_value.get_recipe.side_effect = \
            AttributeError

        self.assertRaises(
            RecipePackageNotValidError, self.command.validate_package, '/tmp')

    def test_call_error(self):
        """Should print RecipePackageNotValidError when raised."""
        self.add_mock('builtins.print')
        error = RecipePackageNotValidError(3, 'test')
        self.add_mock_object(
            self.command,
            'validate_package',
            side_effect=error)

        self.command.make()

        self.mocks['print'].assert_called_once_with(error)

    def test_call_success(self):
        """Should save initfile with proper data."""
        self.command.args = ('somepackage',)
        self.add_mock_object(self.command, 'validate_package')

        self.command.initfile = InitFile()
        self.command.initfile.package = 'somepackage'
        self.command.make()

        testfile = open(InitFile.filename)
        data = json.load(testfile)
        testfile.close()
        self.assertEqual({'package': 'somepackage'}, data)

        os.unlink(InitFile.filename)
