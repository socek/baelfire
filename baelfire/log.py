import logging
from json import dump
from collections import OrderedDict


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


class Logger(object):

    def __init__(self):
        self.common_log = logging.getLogger('common')
        self.task_log = logging.getLogger('task')

        self.init_file_handler()
        self.init_common()
        self.init_task()

    def init_file_handler(self):
        self.file_handler = logging.FileHandler('.baelfire.log')
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    def get_stdout_handler(self, format):
        stdout = logging.StreamHandler()
        stdout.setLevel(logging.INFO)
        formatter = logging.Formatter(format)
        stdout.setFormatter(formatter)
        return stdout

    def init_common(self):
        self.common_log.setLevel(logging.DEBUG)
        self.common_log.addHandler(self.get_stdout_handler('%(message)s'))
        self.common_log.addHandler(self.file_handler)

    def init_task(self):
        self.task_log.setLevel(logging.DEBUG)

        self.task_log.addHandler(self.get_stdout_handler('* %(message)s'))
        self.task_log.addHandler(self.file_handler)

    def info(self, *args, **kwargs):
        return self.common_log.info(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.common_log.error(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.common_log.warning(*args, **kwargs)

    def debug(self, *args, **kwargs):
        return self.common_log.debug(*args, **kwargs)

    def task(self, *args, **kwargs):
        return self.task_log.info(*args, **kwargs)
