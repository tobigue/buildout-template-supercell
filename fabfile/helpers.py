from fabric.api import cd, env, run


def supervisor(command):
    """
    Run a supervisor command.
    """
    if run('if [ -d %s ]; then echo y; else echo n; fi' % env.current) == 'y':
        with cd(env.current):
            run('bin/supervisorctl %s' % command)
