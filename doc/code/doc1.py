from baelfire.task import Task
from baelfire.dependencies import FileDoesNotExists


class FirstTask(Task):

    def create_dependecies(self):
        self.add_dependency(FileDoesNotExists(raw_path='/tmp/me'))

    def build(self):
        print('building...')
        with open('/tmp/me', 'w') as myfile:
            myfile.write('something\n')

FirstTask().run()
