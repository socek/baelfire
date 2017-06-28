import logging

from baelfire.task import Task
from baelfire.dependencies import FileDoesNotExists


class FirstTask(Task):

    def create_dependecies(self):
        self.build_if(FileDoesNotExists(raw_path='/tmp/me'))

    def build(self):
        print('building...')
        with open('/tmp/me', 'w') as myfile:
            myfile.write('something\n')

FORMAT = ' * %(levelname)s %(name)s: %(message)s *'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

if __name__ == '__main__':
    FirstTask().run()
