from soktest import TestCase

from .task import ExampleTask
from ..dependencys import Dependency


class ExampleDependency(Dependency):

    def __init__(self):
        super().__init__()
        self.running = []

    def validate_task(self):
        self.running.append('validate_task')

    def validate_parent(self):
        self.running.append('validate_parent')

    def make(self):
        self.running.append('make')
        return 'make'


class DependencyTest(TestCase):

    def setUp(self):
        super().setUp()
        self.task = ExampleTask()
        self.dependency = ExampleDependency()
        self.dependency.assign_task(self.task)

    def test_init(self):
        dependency = Dependency()

        self.assertEqual(None, dependency.task)
        self.assertEqual(None, dependency.parent)

    def test_assign_task(self):
        """Should assign task"""
        self.assertEqual(self.task, self.dependency.task)

    def test_assign_parent(self):
        """Should assign parent"""
        task = ExampleTask()
        self.dependency.assign_parent(task)
        self.assertEqual(task, self.dependency.parent)

    def test_call(self):
        """Should run validation of task, parent and then run make method."""
        self.assertEqual('make', self.dependency())
        self.assertEqual(
            ['validate_task', 'validate_parent', 'make'],
            self.dependency.running)
