from bdjango.core import BdCore
from bdjango.tasks import StartRunserver
from bdjango.tasks import UpdateRequirements


def update_requirements():
    return UpdateRequirements(BdCore())


def start_runserver():
    return StartRunserver(BdCore())
