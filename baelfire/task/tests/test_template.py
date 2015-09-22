from tempfile import NamedTemporaryFile

from ..template import TemplateTask


class ExampleTemplateTask(TemplateTask):
    source_name = 'source'
    output_name = 'output'

    def __init__(self):
        super().__init__()
        self.source_file = NamedTemporaryFile(delete=False)
        self.source_file.write(
            b"{{paths['source']}}|{{paths['output']}}",
        )
        self.source_file.close()

    def phase_settings(self):
        super().phase_settings()
        self.paths['jinja_templates'] = '/'
        self.paths[self.source_name] = self.source_file.name
        self.paths[self.output_name] = NamedTemporaryFile().name


class TestTemplateTask(object):

    def test_normal(self):
        """
        Source should be a template to output file.
        """
        task = ExampleTemplateTask()
        task.run()

        data = open(task.output, 'r').read()
        assert data == task.source + "|" + task.output

    def test_rebuild_on_template_change(self):
        """
        Task should be rebuild on template change.
        """
        task = ExampleTemplateTask()
        task.run()

        with open(task.source_file.name, 'w') as data:
            data.write('xxx')

        task.run()

        data = open(task.output, 'r').read()
        assert data == 'xxx'
