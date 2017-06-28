from baelfire.dependencies import AlwaysTrue
from baelfire.task import SubprocessTask


class SimpleProccess(SubprocessTask):

    def create_dependecies(self):
        self.build_if(AlwaysTrue())

    def build(self):
        self.popen(['echo', 'something'])

    def _set_default_args(self, args, kwargs):
        kwargs.setdefault('shell', False)
        return args, kwargs


if __name__ == '__main__':
    SimpleProccess().run()
