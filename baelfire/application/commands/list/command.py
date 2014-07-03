from ..command import TriggeredCommand, Command


class ListTasksMixin(object):

    names_minimal_size = 4
    paths_minimal_size = 4

    def tasks_to_print(self):
        return filter(self.get_filter, self.recipe.tasks.values())

    def make(self):
        self.recipe = self.get_recipe()
        sizes = self.count_columns_width()

        text = ''

        template = ' %%-%(names)ds %%-%(paths)ds %%s\n' % sizes

        text += template % ('Name', 'Path', 'Help')
        text += template % ('----', '----', '----')

        for task in self.tasks_to_print():
            text += template % (
                task.name,
                task.get_path(),
                task.help,
            )

        print(text)

    def count_columns_width(self):
        sizes = {
            'names': self.names_minimal_size,
            'paths': self.paths_minimal_size,
        }
        for task in self.tasks_to_print():
            sizes['names'] = max(len(task.name), sizes['names'])
            sizes['paths'] = max(len(task.get_path()), sizes['paths'])

        sizes['names'] += 2
        sizes['paths'] += 2
        return sizes


class ListTasks(TriggeredCommand, ListTasksMixin):

    def __init__(self):
        super().__init__('-l',
                         '--list',
                         help='Lists tasks')

    def get_filter(self, task):
        return not task.hide


class ListAllTasks(TriggeredCommand, ListTasksMixin):

    def __init__(self):
        super().__init__('-a',
                         '--list-all',
                         help='List all tasks.')

    def get_filter(self, task):
        return True


class PathsList(Command, ListTasksMixin):

    def __init__(self):
        super().__init__(
            '-p',
            '--paths',
            help='List all paths (for autocomplete)',
            const='',
            nargs='?')

    def get_filter(self, task):
        return task.get_path().startswith(self.args)

    def make(self):
        self.recipe = self.get_recipe()
        paths = [task.get_path() for task in self.tasks_to_print()]
        if len(paths) > 0:
            print('\n'.join(paths))
