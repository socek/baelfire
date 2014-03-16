class Command(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.kwargs['dest'] = self.name

    def assign_argument(self, parser):
        parser.add_argument(*self.args, **self.kwargs)

    def assign_application(self, application):
        self.application = application

    def __call__(self, args=(), raw_args={}):
        self.args = args
        self.raw_args = raw_args
        self.make()

    @property
    def name(self):
        return self.__class__.__name__
