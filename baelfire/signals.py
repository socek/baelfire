import signal


class SignalHandling(object):

    def __init__(self, recipe):
        self.recipe = recipe
        for _signal in [
            signal.SIGABRT,
            signal.SIGFPE,
            signal.SIGILL,
            signal.SIGINT,
            signal.SIGSEGV,
            signal.SIGTERM
        ]:
            signal.signal(_signal, self.on_signal)

    def send_signal(self, spp, signal):
        try:
            if spp.poll() is None:
                spp.send_signal(signal)
        except OSError:
            pass

    def on_signal(self, signum, frame):
        self.recipe.aborting = True
        if self.recipe._spp is not None:
            self.send_signal(self.recipe._spp, signum)
