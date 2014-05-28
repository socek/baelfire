from .init.models import InitFile, get_recipe_from_url
from baelfire.error import RecipeNotFoundError


class Command(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.kwargs['dest'] = self.name

    def assign_argument(self, parser):
        parser.add_argument(*self.args, **self.kwargs)

    def assign_application(self, application):
        self.application = application

    def __call__(self, args=(), raw_args=None):
        self.args = args
        self.raw_args = raw_args or {}
        self.make()

    @property
    def name(self):
        return self.__class__.__name__

    def get_recipe(self):
        """Gets recipe from command switch or init file."""
        application_recipe = getattr(self.application, 'recipe', None)
        if application_recipe is not None:
            return application_recipe
        elif self.raw_args.get('recipe', None) is not None:
            return get_recipe_from_url(self.raw_args['recipe'])()
        else:
            initfile = InitFile()
            if initfile.is_present():
                initfile.load()
                initfile.install_dependencies()
                return initfile.get_recipe()()

        raise RecipeNotFoundError()


class TriggeredCommand(Command):

    def __init__(self, *args, **kwargs):
        kwargs['action'] = 'store_true'
        super().__init__(*args, **kwargs)

    def __call__(self, args=(), raw_args={}):
        self.args = args
        self.raw_args = raw_args
        if self.args is True:
            self.make()
