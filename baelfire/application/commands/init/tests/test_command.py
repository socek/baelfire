import json
from io import StringIO

from soktest import TestCase

from ..command import Init
from ..models import InitFile
from ..error import RecipePackageNotValidError

PREFIX = 'baelfire.application.commands.init.command.'


class InitTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = Init()
        self.command.initfile = InitFile()
        self.command.initfile.assign('os:path', 'setupy')

    def test_init(self):
        self.assertEqual('Init',
                         self.command.name)
        self.assertEqual(('-i', '--init'), self.command.args)
        self.assertEqual(
            {
                'dest': 'Init',
                'nargs': '+',
                'help': 'Inits package.'
            },
            self.command.kwargs)

    def test_validate_package_success(self):
        """Should return None if no error found."""
        self.assertEqual(None, self.command.validate_package())

    def test_validate_package_bad_url(self):
        """Should raise RecipePackageNotValidError when bad url provided."""
        self.command.initfile.assign('os:path2', 'setupy')

        self.assertRaises(
            RecipePackageNotValidError, self.command.validate_package)

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
        self.command.args = ('testrecipe.all:TestMe', 'testrecipe/setup.py')
        self.add_mock_object(self.command, 'validate_package')
        self.add_mock_object(self.command, 'validate_setup')
        data = StringIO()
        self.add_mock_object(data, 'close')
        self.add_mock('builtins.open', return_value=data)
        self.add_mock('baelfire.application.commands.init.models.Popen')
        self.add_mock_object(
            InitFile, 'is_reinstall_needed', return_value=True)
        self.mocks['Popen'].return_value.returncode = 0

        self.command.make()

        data.seek(0)
        data = json.load(data)

        self.assertEqual({
            'package_url': 'testrecipe.all:TestMe',
            'setup_path': 'testrecipe/setup.py'}, data)

        self.mocks['close'].assert_called_once_with()

    def test_validate_setup_error(self):
        """Should raise RecipePackageNotValidError when setup.py file do not
        exists"""
        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.return_value = False

        self.assertRaises(RecipePackageNotValidError,
                          self.command.validate_setup)
        self.mocks['path'].exists.assert_called_once_with('setupy')

    def test_validate_setup_success(self):
        """Should do nothing when everything is good."""
        self.add_mock(PREFIX + 'path')
        self.mocks['path'].exists.return_value = True
        self.assertEqual(None, self.command.validate_setup())

    def test_validate_setup_when_no_setup_path_set(self):
        """Should do nothing."""
        self.command.initfile.setup_path = None
        self.assertEqual(None, self.command.validate_setup())
