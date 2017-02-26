from baelfire.dependencies.dependency import AlwaysRebuild
from baelfire.dependencies.task import RunBefore
from baelfire.task import SubprocessTask
from baelfire.core import Core


class ScreenCore(Core):

    def phase_settings(self):
        super(ScreenCore, self).phase_settings()
        self.paths.set('exe:screen', ['usr', 'bin', 'screen'], is_root=True)


class ScreenTask(SubprocessTask):
    """
    Start command in detached screen.
    """

    screen_name = None

    def _screen_run(self, *args, **kwargs):
        screen_name = 'S %s' % (self.screen_name,) if self.screen_name else ''
        args[0][0] = (
            '%s -dm%s ' % (self.paths.get('exe:screen'), screen_name) + args[0][0]
        )
        return self.popen(*args, **kwargs)


class AttachScreenTask(SubprocessTask):
    """
    Attach task from screen. Run it first if needed.

    In order to use this, you need to set `detached_task` property, which should
    be the ScreenTask like task.
    """
    detached_task = None

    def create_dependecies(self):
        assert self.detached_task
        self._detached_task = self.detached_task()

        self.add_dependency(RunBefore(self._detached_task))
        self.add_dependency(AlwaysRebuild())

    def _screen_attach(self):
        cmd = '%s -r %s' % (self.paths.get('exe:screen'),
                            self._detached_task.screen_name)
        return self.popen([cmd])

    def build(self):
        self._screen_attach()
