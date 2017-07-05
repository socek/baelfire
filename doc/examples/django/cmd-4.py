from baelfire.application.application import Application

from bdjango.core import BdCore
from bdjango.tasks import AttachCelery
from bdjango.tasks import StartRunserver
from bdjango.tasks import UpdateRequirements


class BdApplication(Application):
    tasks = {
        'update': UpdateRequirements,
        'runserver': StartRunserver,
        'celery': AttachCelery,
    }

    def get_task(self, name):
        task = self.tasks[name]
        return task(BdCore())


def run():
    BdApplication().run()
