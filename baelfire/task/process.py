import signal

from subprocess import Popen

from .task import Task
from baelfire.error import CommandAborted
from baelfire.error import CommandError


class SubprocessTask(Task):
    """
    Task which will run external programs. This task will manage sending
    proccess signals.
    """

    def phase_init(self):
        super(SubprocessTask, self).phase_init()
        self.spp = None
        self.myreport['aborted'] = False
        self.myreport['signal'] = None

    def send_signal(self, signal):
        try:
            if self.spp.poll() is None:
                self.spp.send_signal(signal)
        except OSError:
            pass

    def on_signal(self, signum, frame):
        self.myreport['aborted'] = True
        self.myreport['signal'] = signum
        self.spp and self.send_signal(signum)

    def popen(self, *args, **kwargs):
        """
        Run subprocess.Popen whitin the task.
        """
        args, kwargs = self._set_default_args(args, kwargs)
        self._init_signals()
        self._popen(*args, **kwargs)
        self._post_popen()

    def _set_default_args(self, args, kwargs):
        kwargs.setdefault('shell', True)
        return args, kwargs

    def _init_signals(self):
        for _signal in [
            signal.SIGABRT,
            signal.SIGFPE,
            signal.SIGILL,
            signal.SIGINT,
            signal.SIGSEGV,
            signal.SIGTERM,
        ]:
            signal.signal(_signal, self.on_signal)

    def _popen(self, *args, **kwargs):
        self.spp = Popen(*args, **kwargs)
        self.spp.wait()

    def _post_popen(self):
        if self.myreport['aborted']:
            raise CommandAborted()
        if self.spp.returncode is not 0:
            raise CommandError(self.spp.returncode)
