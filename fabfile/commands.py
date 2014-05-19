from datetime import datetime

from fabric.api import abort, cd, env, run, settings

from .helpers import supervisor


def deploy():
    """
    Deploy the Python backend and start supervisor
    """

    new_version_dir = '%s/%s' % (env.releases,
                                 datetime.now().strftime('%Y%m%d%H%M%S'))
    run('mkdir -p %s' % new_version_dir)

    # prepare or updated the cached copy
    run('git clone %s %s' % (env.git_url, new_version_dir))

    # based on the environment we deploy a certain branch/tag from git
    with cd(new_version_dir):
        if env.env_type in ['testing', 'staging']:
            if not env.git_branch:
                abort('In "%s" environment only branches may be deployed' %
                      env.env_type)
            if env.git_branch != 'master':
                run('git checkout -b %(git_branch)s origin/%(git_branch)s' %
                    env)

        elif env.env_type == 'live':
            if not env.git_tag:
                abort('In "%s" environment only tags may be deployed' %
                      env.env_type)
            run('git checkout -b tag-%(git_tag)s %(git_tag)s' % env)

    with cd(new_version_dir):
        run('make')

    # Stop the current running version
    with settings(warn_only=True):
        supervisor('shutdown')

    # reset the `current` link to the new version
    with cd(env.base_dir):
        run('rm -f current && ln -s %s current' % new_version_dir)

    # Start the new version
    with cd(env.current):
        run('bin/supervisord && sleep 1')

    # Remove the oldest version
    with cd(env.releases):
        releases = run('ls -rt').split('\t')
        if len(releases) > 3:
            run('rm -rf %s/%s' % (env.releases, releases[0]))


def rollback():
    """
    Rollback the current version to the version before.
    """
    with cd(env.base_dir):
        current_version = run('readlink current | sed "s/.*\/\(.*\)/\\1/"')

        # try to get the previous version
        releases = run('ls -t releases').split('\t')
        for i in xrange(len(releases)):
            if releases[i].endswith(current_version):
                previous_version = releases[i + 1]

        # stop the `current` version
        with settings(warn_only=True):
            supervisor('shutdown')

        # install the `old` version
        with cd(env.base_dir):
            run('rm current && ln -s %s/%s current' % (env.releases,
                                                       previous_version))

        # start the `new` version
        with cd(env.current):
            run('bin/supervisord && sleep 1')
