#!/usr/bin/python

import collectd

from lib.DependencyResolver import DependencyResolver
from lib.Collectd.Exporter import Exporter
from lib.Collectd.Plugin import Plugin


def configure(self, conf):
    for node in conf.children:
        try:
            if node.key == 'SocketUrl':
                socket_url = node.values[0]
            elif node.key == 'Timeout':
                timeout = int(node.values[0])
        except Exception as e:
            raise Exception('Failed to load the configuration {0} due to {1}'.format(node.key, e))

    exporter = Exporter(collectd)

    resolver = DependencyResolver.get_Resolver(socket_url, timeout)

    plugin = Plugin(
        resolver.get_DockerStatsClient(),
        resolver.get_DockerFormatter(),
        resolver.get_ContainerStatsStreamPool(),
        exporter
    )

    collectd.register_read(plugin.read)


collectd.register_config(configure)
