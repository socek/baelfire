from jinja2 import Environment
from jinja2 import FileSystemLoader

from baelfire.dependencies import FileChanged
from baelfire.dependencies import FileDoesNotExists
from baelfire.task import FileTask


class BaseTemplateTask(FileTask):

    @property
    def source(self):
        return self.paths.get(self.source_name)

    def jinja(self):
        """Jinja2 environment generator."""
        return Environment(
            loader=self.get_jinja2_loader(),
            keep_trailing_newline=True,
        )

    def get_jinja2_loader(self):
        return FileSystemLoader(self.paths.get('jinja_templates'))

    def build(self):
        template = self.get_template()
        stream = template.stream(**self.generate_context())
        stream.dump(self.output)

    def generate_context(self):
        """Generates data which will be used in the template."""
        context = {}
        context['settings'] = self.settings
        context['paths'] = self.paths
        return context

    def get_template(self):
        return self.jinja().get_template(self.source)


class TemplateTask(BaseTemplateTask):
    """
    Task which generate file from template.
    """

    def create_dependecies(self):
        super(TemplateTask, self).create_dependecies()
        self.add_dependency(FileChanged(self.source_name))


class FirstTemplateTask(BaseTemplateTask):
    """
    Task which generate file from template but only if output does not exists.
    """

    def create_dependecies(self):
        super(FirstTemplateTask, self).create_dependecies()
        self.add_dependency(FileDoesNotExists(self.source_name))
