from supercell.api import Service
from tornado.options import define
from projectname import __options__


class HelloWorldService(Service):

    def bootstrap(self):
        for name, details in __options__["tornado_options"].items():
            define(name, details["value"], help=details.get("help", ""))
        self.environment.config_file_paths.append('conf/')
        self.environment.config_file_paths.append('/etc/projectname/conf/')

    def run(self):

        from modules.hello import WorldGenerator
        self.environment.add_managed_object('world_generator', WorldGenerator())

        from api.hello import HelloWorldHandler
        self.environment.add_handler(r'/', HelloWorldHandler, {})
