from tempfile import NamedTemporaryFile

from ..template import FirstTemplateTask
from ..template import TemplateTask
from baelfire.core import Core


class ExampleCore(Core):
    source_name = 'source'
    output_name = 'output'

    def __init__(self):
        super(ExampleCore, self).__init__()
        self.source_file = NamedTemporaryFile(delete=False)
        self.source_file.write(
            b"{{paths.get('source')}}|{{paths.get('output')}}",
        )
        self.source_file.close()

    def phase_settings(self):
        super(ExampleCore, self).phase_settings()
        self.paths.set('jinja_templates', '', is_root=True)
        self.paths.set(self.source_name, self.source_file.name)
        self.paths.set(self.output_name, NamedTemporaryFile().name)


class ExampleTemplateTask(TemplateTask):
    source_name = 'source'
    output_name = 'output'


class ExampleFirstTemplateTask(FirstTemplateTask):
    source_name = 'source'
    output_name = 'output'


class TestTemplateTask(object):

    def test_normal(self):
        """
        Source should be a template to output file.
        """
        task = ExampleTemplateTask(ExampleCore())
        task.run()

        data = open(task.output, 'r').read()
        assert data == task.source + "|" + task.output

    def test_rebuild_on_template_change(self):
        """
        Task should be rebuild on template change.
        """
        core = ExampleCore()
        task = ExampleTemplateTask(core)
        task.run()

        with open(core.source_file.name, 'w') as data:
            data.write('xxx')

        task.run()

        data = open(task.output, 'r').read()
        assert data == 'xxx'


class TestFirstTemplateTask(object):

    def test_normal(self):
        """
        Source should be a template to output file.
        """
        task = ExampleFirstTemplateTask(ExampleCore())
        task.run()

        data = open(task.output, 'r').read()
        assert data == task.source + "|" + task.output

        with open(task.output, 'w') as fp:
            fp.write('new')

        task = ExampleFirstTemplateTask(ExampleCore())
        task.run()

        data = open(task.output, 'r').read()
        assert data == task.source + "|" + task.output
