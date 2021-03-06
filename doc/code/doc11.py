from baelfire.core import Core
from baelfire.dependencies import AlwaysTrue
from baelfire.filedict import FileDict
from baelfire.task import Task


class MyCore(Core):

    def phase_settings(self):
        super(MyCore, self).phase_settings()
        data = FileDict('.file.yaml')
        data.load(True)
        data.ensure_key_exists('something', 'Description for something')
        data.save()

        self.settings['something'] = data['something']


class MyTask(Task):

    def create_dependecies(self):
        self.build_if(AlwaysTrue())

    def build(self):
        print(self.settings['something'])


if __name__ == '__main__':
    MyTask(MyCore()).run()
