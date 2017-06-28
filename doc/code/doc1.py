from baelfire.task import Task
from baelfire.dependencies import FileDoesNotExists


class FirstTask(Task):

    def create_dependecies(self):
        self.build_if(FileDoesNotExists(raw_path='/tmp/me'))

    def build(self):
        print('building...')
        with open('/tmp/me', 'w') as myfile:
            myfile.write('something\n')

if __name__ == '__main__':
    FirstTask().run()
