class Task(object):

    def __init__(self):
        self.recipe = None
        self.path = None
        self.dependencys = None
        self.kwargs = {}

    def assign_kwargs(self, **kwargs):
        self.kwargs.update(kwargs)

    def assign_recipe(self, recipe):
        self.recipe = recipe
        self.dependencys = []

    def add_dependecy(self, dependency):
        dependency.assign_task(self)
        self.dependencys.append(dependency)

    def get_output_file(self):
        return None

    @property
    def name(self):
        return self.__class__.__name__

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

        for dependency in self.dependencys:
            need_rebuild = need_rebuild or dependency()

        return need_rebuild

    def pre_run(self):
        pass

    def logme(self, force, needed, success):
        logdata = {
            'force': force,
        }
        self.recipe.data_log.add_task(self, logdata)

    def run(self):
        self.pre_run()
        force = self.kwargs.pop('force', False)
        success = False
        needed = self.is_rebuild_needed()

        try:
            if needed or force:
                self.log.task(self.name)
                self.make(**self.kwargs)
                success = True
        finally:
            self.logme(force, needed, success)

    def was_runned(self):
        """Was this task runned?"""
        return self.name in self.recipe.data_log.tasks

    @property
    def paths(self):
        return self.recipe.paths

    @property
    def settings(self):
        return self.recipe.settings

    @property
    def log(self):
        return self.recipe.log
