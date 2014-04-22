from select import select
from subprocess import Popen, PIPE

from .error import CommandError, CommandAborted


class Process(object):

    def __init__(self, task):
        self.task = task
        self.recipe = task.recipe
        self.spp = None

    def prepare_args(self, args, kwargs):
        kwargs['shell'] = kwargs.get('shell', True)

    def pipes(self):
        try:
            return select([self.spp.stdout, self.spp.stderr], [], [])[0]
        except InterruptedError:
            raise CommandAborted()

    def write_to_log(self, pipename, loglevel):
        pipe = getattr(self.spp, pipename)
        log = getattr(self.recipe.log.process_log, loglevel)

        if pipe in self._pipes:
            data = pipe.readline().decode('utf-8').strip()
            log(data)

    def run(self):
        self.spp.wait()

    def post_run(self):
        if self.recipe.aborting is True:
            raise CommandAborted()
        if self.spp.returncode is not 0:
            raise CommandError(self.spp.returncode)

    def __call__(self, *args, **kwargs):
        self.prepare_args(args, kwargs)
        self.spp = Popen(*args, **kwargs)
        self.run()
        self.post_run()
        return self.spp
