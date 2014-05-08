import os
import sys
from jinja2 import Environment, PackageLoader

from baelfire.task import Task
from baelfire.dependencys import FileChanged


class TemplateTask(Task):

    templates_dir = 'templates'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._jinja = None

    def module(self):
        """Module which store templates."""
        return sys.modules[self.recipe.__module__]

    def template_absolute_path(self):
        """Absoluth path to a template."""
        dirname = os.path.dirname(self.module().__file__)
        return os.path.join(dirname,
                            self.templates_dir,
                            self.get_template_path())

    def generate_dependencys(self):
        """Generates FileChanged dependency for template file and task file.
        generate_dependencys method is not needed now."""
        self.add_dependecy(FileChanged(self.template_absolute_path()))
        task_file = sys.modules[self.__module__].__file__
        self.add_dependecy(FileChanged(task_file))

    def jinja(self):
        """Jinja2 environment generator."""
        if self._jinja is None:
            loader = PackageLoader(self.module().__name__,
                                   self.templates_dir)
            self._jinja = Environment(loader=loader)
        return self._jinja

    def generate_data(self):
        """Generates data which will be used in the template."""
        data = {}
        data['settings'] = self.settings
        data['paths'] = self.paths
        return data

    def make(self):
        template = self.jinja().get_template(self.get_template_path())
        stream = template.stream(**self.generate_data())
        stream.dump(self.get_output_file())
