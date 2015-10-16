from .file import FileTask
from .process import SubprocessTask
from .task import Task
from .template import TemplateTask

__all__ = [
    'Task',
    'FileTask',
    'TemplateTask',
    'SubprocessTask',
]
