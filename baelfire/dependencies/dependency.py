class Dependency(object):

    @property
    def name(self):
        """
        Return name of this task.
        """
        return self.__module__ + "." + self.__class__.__name__

    def __init__(self):
        self.task = None
        self.parent = None

    def phase_init(self):
        self.mylog['phase_validation'] = False
        self.mylog['builded'] = False
        self.mylog['success'] = False
        self.mylog['should_build'] = None
        self.mylog['index'] = self.parent.get_index()

    def phase_settings(self):
        pass

    def phase_data(self):
        pass

    def phase_validation(self):
        self.mylog['phase_validation'] = True
        result = self.should_build()
        self.mylog['should_build'] = result
        self.parent.logger.debug(
            'Dependency %(dependency)s result: %(result)r' % {
                'dependency': self.name,
                'result': result,
            }
        )
        return result

    def phase_build(self):
        self.mylog['builded'] = True
        self.build()
        self.mylog['success'] = True

    def set_parent(self, parent):
        self.parent = parent

    @property
    def mylog(self):
        if self.name not in self.parent.mylog['dependencies']:
            self.parent.mylog['dependencies'][self.name] = {}
        return self.parent.mylog['dependencies'][self.name]

    @property
    def settings(self):
        return self.parent.settings

    @property
    def paths(self):
        return self.parent.paths

    def build(self):
        pass


class AlwaysRebuild(Dependency):

    """
    Always rebuild this task.
    """

    def should_build(self):
        return True


class NoRebuild(Dependency):

    """
    This dependency will always return "do not rebuild". It is for testing
    purpose.
    """

    def should_build(self):
        return False
