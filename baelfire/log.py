import os
import logging
from json import dump, load
from collections import OrderedDict


class TaskLogger(object):

    filename = '.baelfire.lastlog.json'

    def __init__(self):
        self.tasks = OrderedDict()

    def add_task(self, task, data):
        self.tasks[task.name] = {
            'name': task.name,
            'path': task.get_path_dotted(),
            'data': data,
            'dependencies': [],
        }

    def add_dependecy(self, task, dependency, data):
        self.tasks[task.name]['dependencies'].append({
            'name': dependency.name,
            'data': data,
        })

    def save(self):
        """Saves tasks log coded in json ordered by tasks execution."""
        data = [task for key, task in self.tasks.items()]
        if len(data) > 0:
            log = open(self.filename, 'w')
            dump(data, log, indent=2)
            log.close()

    @classmethod
    def read(cls):
        """Read lastlog and return data."""
        if not os.path.exists(cls.filename):
            return []
        lastlog = open(cls.filename, 'r')
        data = load(lastlog)
        lastlog.close()
        return data


class Logger(object):
    filename = '.baelfire.log'

    def __init__(self):
        self.common_log = logging.getLogger('common')
        self.task_log = logging.getLogger('task')
        self.process_log = logging.getLogger('process')

        self.init_file_handler()
        self.init_common()
        self.init_task()
        self.init_process()

    def init_file_handler(self):
        self.file_handler = logging.FileHandler(self.filename)
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

    def init_process(self):
        self.process_log.setLevel(logging.DEBUG)
        self.process_log.addHandler(self.get_stdout_handler('%(message)s'))
        self.process_log.addHandler(self.file_handler)

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
