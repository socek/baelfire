from soktest import TestCase

from baelfire import error


class ErrorsTests(TestCase):

    def test_TaskMustHaveOutputFile(self):
        er = error.TaskMustHaveOutputFile('name')
        self.assertEqual(str, type(str(er)))
