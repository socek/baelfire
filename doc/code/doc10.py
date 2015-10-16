from subprocess import Popen

from baelfire.dependencies.dependency import AlwaysRebuild
from baelfire.dependencies.pid import PidIsNotRunning
from baelfire.dependencies.pid import PidIsRunning
from baelfire.task import Task
from baelfire.task.process import SubprocessTask


class ExampleProccess(SubprocessTask):

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        self.popen(['yes'])

proc = Popen(['sleep 0.1'], shell=True)


class RunWhenSleepIsRunning(Task):

    def create_dependecies(self):
        self.add_dependency(PidIsRunning(proc.pid))

    def build(self):
        print("sleep is still running...")


class RunWhenSleepIsNotRunning(Task):

    def create_dependecies(self):
        self.add_dependency(PidIsNotRunning(proc.pid))

    def build(self):
        print("sleep is not running!")

RunWhenSleepIsRunning().run()
RunWhenSleepIsNotRunning().run()
proc.wait()

print("- After Termination")
RunWhenSleepIsRunning().run()
RunWhenSleepIsNotRunning().run()
