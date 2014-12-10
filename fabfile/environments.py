import json
from fabric.api import env


with open("conf/deploy.json") as f:
    config = json.load(f)


env.use_ssh_config = True
env.git_url = config["deploy"]["giturl"]


def testing():
    """
    Testing environment
    """
    env.env_type = 'testing'
    env.forward_agent = True
    env.roledefs = {
        "server": config["testing"]["server"]
    }
    env.base_dir = config["testing"]["basedir"].format(config)
    env.releases = "{}/releases".format(env.base_dir)
    env.current = "{}/current".format(env.base_dir)
    env.user = config["testing"]["user"]
    env.port = config["testing"]["port"]
    env.git_branch = config["testing"]["gitbranch"]


def staging():
    """
    Staging environment
    """
    env.env_type = 'staging'
    env.forward_agent = True
    env.roledefs = {
        "server": config["staging"]["server"]
    }
    env.base_dir = config["staging"]["basedir"].format(config)
    env.releases = "{}/releases".format(env.base_dir)
    env.current = "{}/current".format(env.base_dir)
    env.user = config["staging"]["user"]
    env.port = config["staging"]["port"]
    env.git_branch = config["staging"]["gitbranch"]


def live():
    """
    Live environment
    """
    env.env_type = 'live'
    env.forward_agent = True
    env.roledefs = {
        "server": config["live"]["server"]
    }
    env.base_dir = config["live"]["basedir"].format(config)
    env.releases = "{}/releases".format(env.base_dir)
    env.current = "{}/current".format(env.base_dir)
    env.user = config["live"]["user"]
    env.port = config["live"]["port"]
    env.git_tag = config["live"]["gittag"]
