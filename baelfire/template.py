import os
import sys
from jinja2 import Environment, PackageLoader

from baelfire.task import Task
from baelfire.dependencys import FileChanged


class TemplateTask(Task):

    templates_dir = 'templates'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._env = None

    def get_module(self):
        return sys.modules[self.recipe.__module__]

    def get_template_full_path(self):
        dirname = os.path.dirname(self.get_module().__file__)
        return os.path.join(dirname,
                            self.templates_dir,
                            self.get_template_path())

    def _generate_dependencys(self):
        self.add_dependecy(FileChanged(self.get_template_full_path()))
        self.add_dependecy(FileChanged(self.get_module().__file__))

        getattr(self, 'generate_dependencys', lambda: None)()

    def get_env(self):
        if self._env is None:
            loader = PackageLoader(self.get_module().__name__,
                                   self.templates_dir)
            self._env = Environment(loader=loader)
        return self._env

    def get_data(self):
        data = {}
        data['settings'] = self.settings
        data['paths'] = self.paths
        return data

    def make(self):
        env = self.get_env()
        template = env.get_template(self.get_template_path())
        stream = template.stream(**self.get_data())
        stream.dump(self.get_output_file())
