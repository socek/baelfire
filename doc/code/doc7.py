from baelfire.dependencies import TaskDependency
from baelfire.task import FileTask
from baelfire.task import TemplateTask


class CreateSource(FileTask):
    output_name = 'source'

    def build(self):
        with open(self.output, 'w') as output:
            output.write("{{paths['source']}}\n")
            output.write("{{paths['output']}}\n")
            output.write("{{myvar}}\n")


class Something(TemplateTask):
    source_name = 'source'
    output_name = 'output'

    def create_dependecies(self):
        super().create_dependecies()
        self.add_dependency(TaskDependency(CreateSource()))

    def generate_context(self):
        context = super().generate_context()
        context['myvar'] = 'my var 10'
        return context

    def phase_settings(self):
        super().phase_settings()
        self.paths['source'] = 'source.txt'
        self.paths['output'] = 'output.txt'

Something().run()
