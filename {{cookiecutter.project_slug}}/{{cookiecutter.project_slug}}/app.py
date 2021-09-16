import sys
import os

dir_prefix = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(dir_prefix, "./pb"))

from concurrent import futures
import logging
import grpc
from {{cookiecutter.project_slug}}.plogger import get_logger
from {{cookiecutter.project_slug}}.service import Service
from traitlets.config import Application
from traitlets import (
    Integer,
    Unicode,
    Dict,
    default
)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

aliases = {
    'log-level': 'Application.log_level',
    'ip': 'ExampleApplication.ip',
    'port': 'ExampleApplication.port',
    'workers': 'ExampleApplication.workers',
}

flags = {
    'debug': (
        {'Application': {'log_level': logging.DEBUG}},
        "set log level to logging.DEBUG (maximize logging output)",
    ),
}


class ExampleApplication(Application):
    name = 'Example-Application'
    version = "0.1.0"
    description = """An application example
    """
    plogger = get_logger("Application")

    aliases = Dict(aliases)
    flags = Dict(flags)

    ip = Unicode(
        '0.0.0.0', help="Host IP address for listening (default 0.0.0.0)."
    ).tag(config=True)

    port = Integer(
        50052, help="Port (default 50052)."
    ).tag(config=True)

    workers = Integer(
        10, help="Max workers."
    ).tag(config=True)

    # the grpc server handle
    server = None

    @default('log_level')
    def _log_level_default(self):
        return logging.DEBUG

    @default('log_datefmt')
    def _log_datefmt_default(self):
        """Exclude date from default date format"""
        return "%Y-%m-%d %H:%M:%S"

    @default('log_format')
    def _log_format_default(self):
        """override default log format to include time"""
        return "[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s"

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)

        logger = logging.getLogger('{{cookiecutter.project_slug}}')
        logger.propagate = True
        logger.parent = self.log
        logger.setLevel(self.log.level)

    def start(self, argv=None):
        self.initialize(argv)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.workers))
        Service.add_to_server(self, self.server)

        self.server.add_insecure_port('%s:%d' % (self.ip, self.port))

        self.server.start()
        self.plogger.info("Spark Sampling Server Listening On %s:%s..." %
                          (self.ip, self.port))
        self.server.wait_for_termination()

    @classmethod
    def launch(cls, argv=None):
        self = cls.instance()
        self.start(argv)


main = ExampleApplication.launch

if __name__ == '__main__':
    main()
