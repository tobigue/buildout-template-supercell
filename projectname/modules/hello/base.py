import logging

from tornado import gen


class WorldGenerator(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @gen.coroutine
    def get_world(self):
        self.logger.info("Generating world...")
        raise gen.Return("world")
