from fabric.api import roles

from .commands import deploy, rollback
from .environment import testing, staging, live


@roles('server')
def deployfe():
    deploy()


@roles('server')
def rollbackfe():
    rollback()
