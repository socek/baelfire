from os.path import dirname
from baelfire.core import Core


class BdCore(Core):

    def phase_settings(self):
        super(BdCore, self).phase_settings()
        self.paths.set('project', self.get_project_dir(), is_root=True)

        self.paths.set('venv', 'venv_bdjango', parent='project')
        self.paths.set('venv:bin', 'bin', parent='venv')
        self.paths.set('exe:python', 'python', parent='venv:bin')

        self.paths.set('setuppy', 'setup.py', parent='project')

        self.paths.set('bdjango', 'bdjango', parent='project')
        self.paths.set('flags', 'flags', parent='bdjango')
        self.paths.set('flags:requirements', 'req.flag', parent='flags')

    def get_project_dir(self):
        project_dir = __file__
        for index in range(2):
            project_dir = dirname(project_dir)
        return project_dir
