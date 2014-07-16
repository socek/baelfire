import json
from mock import MagicMock
from os import unlink, path
from soktest import TestCase

from ..models import InitFile
from ..error import RecipeInstallError
from baelfire.error import RecipeNotFoundError

PREFIX = 'baelfire.application.commands.init.models.'


class InitFileTest(TestCase):

    def setUp(self):
        super().setUp()
        self.initfile = InitFile()
        self.add_mock_object(self.initfile, 'filename', '/tmp/.bael.init')

    def tearDown(self):
        if path.exists(self.initfile.filename):
            unlink(self.initfile.filename)
        super().tearDown()

    def test_init(self):
        self.assertEqual(None, self.initfile.package_url)
        self.assertEqual(None, self.initfile.setup_path)
        self.assertEqual(None, self.initfile.recipe)

    def test_to_dict(self):
        """Should return proper dict with all the nessesery data"""
        self.initfile.assign('package.url', 'setup/path')

        self.assertEqual(
            {'package_url': 'package.url', 'setup_path': 'setup/path'},
            self.initfile.to_dict())

    def test_from_dict(self):
        """Should unpack all the data from proper dict"""
        self.initfile.from_dict(
            {'package_url': 'package.url', 'setup_path': 'setup/path'})

        self.assertEqual('package.url', self.initfile.package_url)
        self.assertEqual('setup/path', self.initfile.setup_path)

    def test_save(self):
        """Should save initfile data to a '.bael.init' file with json
        encoded"""
        self.initfile.assign('package.url', 'setup/path')
        self.initfile.save()

        testfile = open(self.initfile.filename)
        data = json.load(testfile)
        testfile.close()
        self.assertEqual(
            {'package_url': 'package.url', 'setup_path': 'setup/path'}, data)

    def test_load(self):
        """Shouls load initfile data from a proper '.bael.init' file with
        json encoded"""
        testfile = open(self.initfile.filename, 'w')
        json.dump(
            {'package_url': 'mypackage2', 'setup_path': 'path'}, testfile)
        testfile.close()

        self.initfile.load()

        self.assertEqual('mypackage2', self.initfile.package_url)
        self.assertEqual('path', self.initfile.setup_path)

    def test_get_recipe_with_import(self):
        """Should import recipe where package_url points to."""
        self.initfile.assign('package.url:cls', 'setup/path')
        self.add_mock(PREFIX + 'import_module')
        recipe = self.initfile.get_recipe()

        self.assertEqual(
            self.mocks['import_module'].return_value.cls,
            recipe,
        )
        self.mocks['import_module'].assert_called_once_with('package.url')

    def test_get_recipe_without_import(self):
        self.initfile.assign('package:class', 'setup_path')
        self.initfile.recipe = MagicMock()

        recipe = self.initfile.get_recipe()

        self.assertEqual(self.initfile.recipe, recipe)

    def test_get_recipe_no_recipe_found(self):
        """Should raise BadRecipePathError when import error raised."""
        self.initfile.assign('package:cls', 'setup_path')
        self.add_mock(PREFIX + 'import_module')
        self.mocks['import_module'].return_value = object()

        self.assertRaises(RecipeNotFoundError, self.initfile.get_recipe)

    def test_is_present(self):
        """Should return true if init file is present."""
        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.return_value = True

        self.assertEqual(True, self.initfile.is_present())
        self.mocks['path'].exists.assert_called_once_with('/tmp/.bael.init')

    def test_is_present_failed(self):
        """Should return false if init file is missing."""
        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.return_value = False

        self.assertEqual(False, self.initfile.is_present())
        self.mocks['path'].exists.assert_called_once_with('/tmp/.bael.init')

    def test_install_dependencies_not_needed(self):
        """Should do nothing when reinstall is not required."""
        self.add_mock_object(
            self.initfile, 'is_reinstall_needed', return_value=False)

        self.assertEqual(None, self.initfile.install_dependencies())

    def test_install_dependencies_test_failed(self):
        """Should raise RecipeInstallError when test command failed."""
        self.add_mock_object(
            self.initfile, 'is_reinstall_needed', return_value=True)

        self.add_mock(PREFIX + 'Popen')
        self.mocks['Popen'].return_value.returncode = 1

        self.initfile.assign('package.url', 'setup/path')
        self.assertRaises(
            RecipeInstallError, self.initfile.install_dependencies)
        self.mocks['Popen'].assert_called_once_with(
            ['python', 'setup/path', 'test'])

    def test_install_dependencies_test_success(self):
        """Should save initfile when test command successed."""
        self.add_mock_object(
            self.initfile, 'is_reinstall_needed', return_value=True)

        self.add_mock(PREFIX + 'Popen')
        self.mocks['Popen'].return_value.returncode = 0

        self.initfile.assign('package.url', 'setup/path')
        self.initfile.install_dependencies()

        self.mocks['Popen'].assert_called_once_with(
            ['python', 'setup/path', 'test'])

    def test_is_reinstall_needed_when_filename_not_exists(self):
        """Should return True when filename do not exists."""
        self.add_mock(PREFIX + 'path')
        self.initfile.setup_path = 'something'
        self.mocks['path'].exists.return_value = False

        self.assertEqual(True, self.initfile.is_reinstall_needed())

        self.mocks['path'].exists.assert_called_once_with(
            self.initfile.filename)

    def test_is_reinstall_needed_when_setup_is_older_then_filename(self):
        """Should return True when setup is older then filename."""
        def getmtime_mock(filename):
            if filename == self.initfile.filename:
                return 1
            else:
                return 2
        self.add_mock(PREFIX + 'path')
        self.initfile.setup_path = 'something'
        self.mocks['path'].exists.return_value = True
        self.mocks['path'].getmtime.side_effect = getmtime_mock

        self.assertEqual(True, self.initfile.is_reinstall_needed())

        self.mocks['path'].exists.assert_called_once_with(
            self.initfile.filename)

    def test_is_reinstall_needed_when_filename_is_older_then_setup(self):
        """Should return False when filename is older then setup."""
        def getmtime_mock(filename):
            if filename == self.initfile.filename:
                return 2
            else:
                return 1
        self.add_mock(PREFIX + 'path')
        self.initfile.setup_path = 'something'
        self.mocks['path'].exists.return_value = True
        self.mocks['path'].getmtime.side_effect = getmtime_mock

        self.assertEqual(False, self.initfile.is_reinstall_needed())

        self.mocks['path'].exists.assert_called_once_with(
            self.initfile.filename)

    def test_is_reinstall_needed_when_setup_path_is_none(self):
        """Should return False when setup_path is not set."""
        self.initfile.setup_path = None
        self.assertEqual(False, self.initfile.is_reinstall_needed())
