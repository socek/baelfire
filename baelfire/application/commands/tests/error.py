from soktest import TestCase

from ..error import RecipePackageNotValidError


class RecipePackageNotValidErrorTest(TestCase):

    def test_str(self):
        """Should return string from .codes depend on .code"""
        error = RecipePackageNotValidError(1, 'myname')

        self.assertEqual(
            'package does not exist: myname', str(error))
