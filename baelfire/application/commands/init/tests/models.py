import json
from mock import MagicMock
from os import unlink, path
from soktest import TestCase

from ..models import InitFile

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
        self.assertEqual(None, self.initfile.package)
        self.assertEqual(None, self.initfile.module)

    def test_to_dict(self):
        """Should return proper dict with all the nessesery data"""
        self.initfile.package = 'mypackage'

        self.assertEqual({'package': 'mypackage'}, self.initfile.to_dict())

    def test_from_dict(self):
        """Should unpack all the data from proper dict"""
        self.initfile.from_dict({'package': 'mypackage'})

        self.assertEqual('mypackage', self.initfile.package)

    def test_save(self):
        """Should save initfile data to a '.bael.init' file with json
        encoded"""
        self.initfile.package = 'myawsomepackage'
        self.initfile.save()

        testfile = open(self.initfile.filename)
        data = json.load(testfile)
        testfile.close()
        self.assertEqual({'package': 'myawsomepackage'}, data)

    def test_load(self):
        """Shouls load initfile data from a proper '.bael.init' file with
        json encoded"""
        testfile = open(self.initfile.filename, 'w')
        json.dump({'package': 'mypackage2'}, testfile)
        testfile.close()

        self.initfile.load()

        self.assertEqual('mypackage2', self.initfile.package)

    def test_get_recipe_with_import(self):
        """Should import package and return recipe which should be in
        setup.py"""
        self.initfile.package = 'mypackage'
        self.add_mock(PREFIX + 'import_module')
        recipe = self.initfile.get_recipe()

        self.assertEqual(
            self.mocks['import_module'].return_value.recipe,
            recipe,
        )
        self.mocks['import_module'].assert_called_once_with('mypackage.setup')

    def test_get_recipe_without_import(self):
        self.initfile.package = 'mypackage'
        self.add_mock('builtins.__import__')
        self.initfile.module = MagicMock()

        recipe = self.initfile.get_recipe()

        self.assertEqual(self.initfile.module.recipe, recipe)

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
