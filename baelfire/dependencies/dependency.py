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
        self.myreport = {
            'name': self.name,
        }

    def phase_init(self):
        self.myreport['phase_validation'] = False
        self.myreport['builded'] = False
        self.myreport['success'] = False
        self.myreport['should_build'] = None
        self.myreport['index'] = self.parent.get_index()

    def phase_data(self):
        pass

    def phase_validation(self):
        self.myreport['phase_validation'] = True
        result = self.should_build()
        self.myreport['should_build'] = result
        self.parent.logger.debug(
            'Dependency %(dependency)s result: %(result)r' % {
                'dependency': self.name,
                'result': result,
            }
        )
        return result

    def phase_build(self):
        self.myreport['builded'] = True
        self.build()
        self.myreport['success'] = True

    def set_parent(self, parent):
        self.parent = parent

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
