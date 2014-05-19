import tornado.testing

from projectname.modules.hello import WorldGenerator

from test_projectname.utils import log_stderr


class TestWorldGenerator(tornado.testing.AsyncTestCase):

    @tornado.testing.gen_test
    @log_stderr
    def test_get_world(self):
        world_generator = WorldGenerator()
        world = yield world_generator.get_world()
        assert world == "world"
