from subprocess import Popen

from baelfire.dependencies.dependency import AlwaysTrue
from baelfire.dependencies.pid import PidIsNotRunning
from baelfire.dependencies.pid import PidIsRunning
from baelfire.task import Task
from baelfire.task.process import SubprocessTask

proc = Popen(['sleep 0.1'], shell=True)


class ExampleProccess(SubprocessTask):

    def create_dependecies(self):
        self.build_if(AlwaysTrue())

    def build(self):
        self.popen(['yes'])


class RunWhenSleepIsRunning(Task):

    def create_dependecies(self):
        self.build_if(PidIsRunning(proc.pid))

    def build(self):
        print("sleep is still running...")


class RunWhenSleepIsNotRunning(Task):

    def create_dependecies(self):
        self.build_if(PidIsNotRunning(proc.pid))

    def build(self):
        print("sleep is not running!")


if __name__ == '__main__':
    RunWhenSleepIsRunning().run()
    RunWhenSleepIsNotRunning().run()
    proc.wait()

    print("- After Termination")
    RunWhenSleepIsRunning().run()
    RunWhenSleepIsNotRunning().run()
