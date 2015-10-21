from baelfire.task import Task
from baelfire.dependencies import AlwaysRebuild
from baelfire.filedict import FileDict


class MyTask(Task):

    def phase_settings(self):
        super().phase_settings()
        data = FileDict('.file.yaml')
        data.load(True)
        data.ensure_key_exists('something', 'Description for something')
        data.save()

        self.settings['something'] = data['something']

    def create_dependecies(self):
        self.add_dependency(AlwaysRebuild())

    def build(self):
        print(self.settings['something'])

MyTask().run()
