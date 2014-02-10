from .command import Command


class Init(Command):

    def __init__(self):
        super().__init__('init',
                         '-i',
                         '--init',
                         dest='init',
                         nargs=1,
                         help='Inits package.')

    def make(self):
        pass
