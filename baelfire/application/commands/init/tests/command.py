import os
import json

from soktest import TestCase

from ..command import Init
from ..models import InitFile
from ..error import RecipePackageNotValidError
from baelfire.error import RecipeNotFoundError

PREFIX = 'baelfire.application.commands.init.command.'


class InitTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = Init()

    def test_init(self):
        self.assertEqual('Init',
                         self.command.name)
        self.assertEqual(('-i', '--init'), self.command.args)
        self.assertEqual(
            {
                'dest': 'Init',
                'nargs': 2,
                'help': 'Inits package.'
            },
            self.command.kwargs)

    def test_validate_package_success(self):
        """Should return None if no error found."""
        self.command.initfile = InitFile()
        self.command.initfile.assign('os:path', 'setupy')

        self.assertEqual(None, self.command.validate_package())

    def test_validate_package_bad_url(self):
        """Should raise RecipePackageNotValidError when bad url provided."""
        self.command.initfile = InitFile()
        self.command.initfile.assign('os:path2', 'setupy')

        self.assertRaises(
            RecipeNotFoundError, self.command.validate_package)

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
        self.command.args = ('package.url', 'setup/path')
        self.add_mock_object(self.command, 'validate_package')

        testfile = open(InitFile.filename)
        data = json.load(testfile)
        testfile.close()
        self.assertEqual({
            'package_url': 'testrecipe.all:TestMe',
            'setup_path': 'testrecipe/setup.py'}, data)

        os.unlink(InitFile.filename)
