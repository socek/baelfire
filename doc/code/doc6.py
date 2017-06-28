from os import getcwd

from baelfire.core import Core
from baelfire.dependencies import TaskRebuilded
from baelfire.task import FileTask
from baelfire.task import TemplateTask


class MyCore(Core):

    def phase_settings(self):
        super().phase_settings()
        self.paths.set('base', getcwd(), is_root=True)
        self.paths.set('source', 'source.txt', 'base')
        self.paths.set('output', 'output.txt', 'base')


class CreateSource(FileTask):
    output_name = 'source'

    def build(self):
        with open(self.output, 'w') as output:
            output.write("{{paths.get('source')}}\n")
            output.write("{{paths.get('output')}}\n")
            output.write("{{my_context}}\n")


class Something(TemplateTask):
    source_name = 'source'
    output_name = 'output'

    def create_dependecies(self):
        super().create_dependecies()
        self.build_if(TaskRebuilded(CreateSource()))

    def generate_context(self):
        context = super(Something, self).generate_context()
        context['my_context'] = 'this is my context'
        return context


if __name__ == '__main__':
    Something(MyCore()).run()
