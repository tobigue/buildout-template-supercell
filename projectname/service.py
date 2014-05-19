from supercell.api import Service


class HelloWorldService(Service):

    def bootstrap(self):
        self.environment.config_file_paths.append('conf/')

    def run(self):

        from modules.hello import WorldGenerator
        self.environment.add_managed_object('world_generator', WorldGenerator())

        from api.hello import HelloWorldHandler
        self.environment.add_handler(r'/', HelloWorldHandler, {})
