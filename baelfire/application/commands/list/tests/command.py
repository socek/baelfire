from mock import MagicMock

from soktest import TestCase

from ..command import ListTasks


class ListTasksTest(TestCase):

    def setUp(self):
        super().setUp()
        self.command = ListTasks()
        self.add_mock_object(self.command, 'get_recipe')

    def test_get_tasks_to_print(self):
        """Should return only tasks which is not hidden."""
        task_1 = MagicMock()
        task_1.hide = False
        task_2 = MagicMock()
        task_2.hide = True
        self.command.recipe = self.command.get_recipe()
        self.command.recipe.tasks.values.return_value = [task_1, task_2]

        tasks = self.command.get_tasks_to_print()

        self.assertEqual([task_1, ], list(tasks))

    def test_count_columns_width(self):
        """Should return max lenght of names and paths +2 spaces."""
        task_1 = MagicMock()
        task_1.name = 'my name'
        task_1.get_path.return_value = 'short path'
        task_2 = MagicMock()
        task_2.name = 'short'
        task_2.get_path.return_value = 'very long path'

        self.add_mock_object(
            self.command,
            'get_tasks_to_print',
            return_value=[task_1, task_2])

        sizes = self.command.count_columns_width()
        self.assertEqual({
            'names': 9,
            'paths': 16,
        }, sizes)

    def test_make(self):
        """Should pretty print all tasks."""
        task_1 = MagicMock()
        task_1.name = 'my name'
        task_1.get_path.return_value = 'short path'
        task_1.help = 'my help'

        self.add_mock_object(
            self.command,
            'get_tasks_to_print',
            return_value=[task_1])

        self.add_mock('builtins.print')

        self.command.make()
        self.mocks['print'].assert_called_once_with(
            """ Name      Path         Help
 ----      ----         ----
 my name   short path   my help
""")
