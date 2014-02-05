class Task(object):

    def __init__(self):
        self.recipe = None
        self.path = None

    def set_recipe(self, recipe):
        self.recipe = recipe

    @property
    def paths(self):
        return self.recipe.paths

    @property
    def settings(self):
        return self.recipe.settings

    def get_path(self):
        """get_path(self) -> str
        Returns path (for using in command line) of the tasks provided by class
        value path, or just classname if path == None.
        """
        if self.path is None:
            return '/' + self.__class__.__name__.lower()
        else:
            return self.path

    def is_rebuild_needed(self):
        need_rebuild = False

        for dependency in self.get_dependencys():
            need_rebuild = need_rebuild or dependency(self)

        return need_rebuild
