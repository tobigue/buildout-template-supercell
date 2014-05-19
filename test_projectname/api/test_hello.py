import json
from unittest import TestCase
from tornado.testing import AsyncHTTPTestCase
import mock

from tornado import gen
from supercell.api import Environment

from projectname.scripts import start_app
from projectname.api import HelloWorldHandler

from test_projectname.utils import log_stderr


class ServiceTest(TestCase):

    @mock.patch('tornado.ioloop.IOLoop.instance')
    def test_start_app(self, ioloop_instance_mock):
        start_app()


class HelloWorldHandlerMock(HelloWorldHandler):

    def initialize(self, *args, **kwargs):
        self.application.config = mock.Mock()
        self.application.environment = mock.Mock()
        self.environment.get_expires_info = mock.Mock()
        self.environment.get_expires_info.return_value = None
        self.environment.world_generator = mock.Mock()
        super(HelloWorldHandlerMock, self).initialize(*args, **kwargs)

        @gen.coroutine
        def get_world(*args, **kwargs):
            raise gen.Return("world")
        self.environment.world_generator.get_world = get_world


class HelloWorldHandlerErrorMock(HelloWorldHandler):

    def initialize(self, *args, **kwargs):
        self.application.config = mock.Mock()
        self.application.environment = mock.Mock()
        self.environment.get_expires_info = mock.Mock()
        self.environment.get_expires_info.return_value = None
        self.environment.world_generator = mock.Mock()
        super(HelloWorldHandlerErrorMock, self).initialize(*args, **kwargs)

        @gen.coroutine
        def get_world_error(*args, **kwargs):
            raise StandardError("Error in get_world.")
        self.environment.world_generator.get_world = get_world_error


class TestHelloWorldHandler(AsyncHTTPTestCase):

    def get_app(self):
        env = Environment()
        env.add_handler(r'/', HelloWorldHandlerMock)
        env.add_handler(r'/error', HelloWorldHandlerErrorMock)
        return env.get_application()

    @log_stderr
    def test_get(self):
        response = self.fetch('/', method="GET")
        assert response.code == 200
        assert response.body == json.dumps({"hello": "world"})

    @log_stderr
    def test_get_error(self):
        response = self.fetch('/error', method="GET")
        assert response.code == 500
        assert json.loads(response.body) == {
            "error": True,
            "message": "Error in get_world."
        }
