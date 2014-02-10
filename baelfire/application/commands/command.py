class Command(object):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def assign_argument(self, parser):
        parser.add_argument(*self.args, **self.kwargs)

    def assign_application(self, application):
        self.application = application

    def __call__(self, args=()):
        self.args = args
        self.make()
