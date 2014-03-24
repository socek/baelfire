from importlib import import_module

from .init.models import InitFile


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

    def get_recipe(self):
        """Gets recipe from command switch or init file."""
        if 'recipe' in self.raw_args and self.raw_args['recipe'] is not None:
            return import_module(self.raw_args['recipe']).recipe()
        else:
            initfile = InitFile()
            if initfile.is_present():
                initfile.load()
                return initfile.get_recipe()()
        return None


class TriggeredCommand(Command):

    def __init__(self, *args, **kwargs):
        kwargs['action'] = 'store_true'
        super().__init__(*args, **kwargs)

    def __call__(self, args=(), raw_args={}):
        self.args = args
        self.raw_args = raw_args
        if self.args is True:
            self.make()
