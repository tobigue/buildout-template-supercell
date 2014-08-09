from fabric.api import roles

from .commands import deploy, rollback
from .environments import testing, staging, live


@roles('server')
def deployfe():
    deploy()


@roles('server')
def rollbackfe():
    rollback()
