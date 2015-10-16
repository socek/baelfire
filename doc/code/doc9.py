from baelfire.dependencies import AlwaysRebuild
from baelfire.task import SubprocessTask


class SimpleProccess(SubprocessTask):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        self.popen(['echo', 'something'])

    def _set_default_args(self, args, kwargs):
        kwargs.setdefault('shell', False)
        return args, kwargs


SimpleProccess().run()
