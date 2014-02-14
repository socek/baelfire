import json
from mock import MagicMock
from os import unlink, path
from soktest import TestCase

from ..models import InitFile


class InitFileTest(TestCase):

    def setUp(self):
        super().setUp()
        self.initfile = InitFile()
        self.add_mock_object(self.initfile, 'filename', '/tmp/.beal.init')

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
        """Should save initfile data to a '.beal.init' file with json
        encoded"""
        self.initfile.package = 'myawsomepackage'
        self.initfile.save()

        testfile = open(self.initfile.filename)
        data = json.load(testfile)
        testfile.close()
        self.assertEqual({'package': 'myawsomepackage'}, data)

    def test_load(self):
        """Shouls load initfile data from a proper '.beal.init' file with
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
        self.add_mock('builtins.__import__')
        recipe = self.initfile.get_recipe()

        self.assertEqual(
            self.mocks['__import__'].return_value.setup.recipe,
            recipe,
        )
        self.mocks['__import__'].assert_called_once()

    def test_get_recipe_without_import(self):
        self.initfile.package = 'mypackage'
        self.add_mock('builtins.__import__')
        self.initfile.module = MagicMock()

        recipe = self.initfile.get_recipe()

        self.assertEqual(self.initfile.module.recipe, recipe)
