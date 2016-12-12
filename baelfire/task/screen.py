from baelfire.dependencies.dependency import AlwaysRebuild
from baelfire.dependencies.task import RunBefore
from baelfire.task import SubprocessTask


class ScreenTask(SubprocessTask):

    screen_name = None

    def phase_settings(self):
        super(ScreenTask, self).phase_settings()
        self.paths['exe:screen'] = ['/usr', 'bin', 'screen']

    def _screen_run(self, *args, **kwargs):
        screen_name = 'S %s' % (self.screen_name,)
        args[0][0] = (
            '%s -dm%s ' % (self.paths['exe:screen'], screen_name) + args[0][0]
        )
        return self.popen(*args, **kwargs)


class RetachScreenTask(SubprocessTask):
    detached_task = None

    def create_dependecies(self):
        self._detached_task = self.detached_task()

        self.add_dependency(RunBefore(self._detached_task))
        self.add_dependency(AlwaysRebuild())

    def _screen_detach(self):
        cmd = '%s -r %s' % (self.paths['exe:screen'], self._detached_task.screen_name)
        return self.popen([cmd])

    def build(self):
        self._screen_detach()
