import os
import sys
from jinja2 import Environment, FileSystemLoader

from baelfire.task import Task
from baelfire.dependencies import FileChanged


class TemplateTask(Task):

    def __init__(self, *args, **kwargs):
        self.check_template = kwargs.pop('check_template', True)
        super().__init__(*args, **kwargs)
        self._jinja = None

    def template_absolute_path(self):
        """Absoluth path to a template."""
        return os.path.join(self.recipe_paths['templates'],
                            self.get_template_path())

    def generate_dependencies(self):
        """Generates FileChanged dependency for template file and task file.
        generate_dependencies method is not needed now."""
        if self.check_template is True:
            self.add_dependecy(FileChanged(self.template_absolute_path()))
            task_file = sys.modules[self.__module__].__file__
            self.add_dependecy(FileChanged(task_file))

    def jinja(self):
        """Jinja2 environment generator."""
        if self._jinja is None:
            loader = FileSystemLoader(self.recipe_paths['templates'])
            self._jinja = Environment(loader=loader)
        return self._jinja

    def generate_data(self):
        """Generates data which will be used in the template."""
        data = {}
        data['settings'] = self.settings
        data['paths'] = self.paths
        data['recipe_paths'] = self.recipe_paths
        return data

    def make(self):
        template = self.jinja().get_template(self.get_template_path())
        stream = template.stream(**self.generate_data())
        stream.dump(self.get_output_file())
