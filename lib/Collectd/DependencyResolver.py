from Exporter import Exporter
from LogHandler import LogHandler

import logging


class DependencyResolver:
    resolver = None

    @classmethod
    def get_Resolver(cls, collectd):
        if cls.resolver is None:
            cls.resolver = DependencyResolver(collectd)

        return cls.resolver

    def __init__(self, collectd):
        self.collectd = collectd

        self.exporter = None
        self.logger = None

    def get_Exporter(self):
        if self.exporter is None:
            self.exporter = Exporter(self.collectd)

        return self.exporter

    def get_Logger(self):
        if self.logger is None:
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            handler = LogHandler('collectd-docker-stats-plugin', self.collectd)
            logger.addHandler(handler)

            self.logger = logger

        return self.logger
