from collections import OrderedDict
from json import dump


class TaskLogger(object):

    filename = '.lastlog.json'

    def __init__(self):
        self.tasks = OrderedDict()

    def add_task(self, task, data):
        self.tasks[task.name] = {
            'name': task.name,
            'data': data,
            'dependencys': [],
        }

    def add_dependecy(self, task, dependency, data):
        self.tasks[task.name]['dependencys'].append({
            'name': dependency.name,
            'data': data,
        })

    def save(self):
        """Saves tasks log coded in json ordered by tasks execution."""
        log = open(self.filename, 'w')
        data = [task for key, task in self.tasks.items()]
        dump(data, log)
        log.close()
