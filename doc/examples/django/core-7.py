from os.path import dirname

from baelfire.task.screen import ScreenCore


class BdCore(ScreenCore):

    def phase_settings(self):
        super(BdCore, self).phase_settings()
        self.paths.set('project', self.get_project_dir(), is_root=True)

        self.paths.set('venv', 'venv_bdjango', parent='project')
        self.paths.set('venv:bin', 'bin', parent='venv')
        self.paths.set('exe:python', 'python', parent='venv:bin')
        self.paths.set('exe:pip', 'pip', parent='venv:bin')
        self.paths.set('exe:celery', 'celery', parent='venv:bin')

        self.paths.set('setuppy', 'setup.py', parent='project')
        self.paths.set('requirementst_production', 'requirements.txt', parent='project')

        self.paths.set('bdjango', 'bdjango', parent='project')
        self.paths.set('flags', 'flags', parent='bdjango')
        self.paths.set('flags:requirements', 'req.flag', parent='flags')
        self.paths.set('flags:setuppy', 'setuppy.flag', parent='flags')
        self.paths.set('flags:migrations', 'migrations.flag', parent='flags')

        self.paths.set('pid:celery', 'celery.pid', parent='flags')

        self.paths.set('src', 'mysite', parent='project')
        self.paths.set('manage', 'manage.py', parent='src')

    def get_project_dir(self):
        project_dir = __file__
        for index in range(2):
            project_dir = dirname(project_dir)
        return project_dir
