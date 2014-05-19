from supercell.api import async
from supercell.api import provides
from supercell.api import RequestHandler
from supercell.api import Return
from supercell.api import Error

from ..models import HelloWorld


@provides('application/json', default=True)
class HelloWorldHandler(RequestHandler):

    @async
    def get(self):
        try:
            world = yield self.environment.world_generator.get_world()
        except StandardError as e:
            self.logger.error(e, exc_info=True)
            raise Error(500, additional={"message": unicode(e)})

        raise Return(HelloWorld({"hello": world}))
