#!/usr/bin/python

import collectd

from lib.DependencyResolver import DependencyResolver
from lib.Collectd.Exporter import Exporter
from lib.Collectd.Plugin import Plugin

exporter = Exporter(collectd)

resolver = DependencyResolver.get_Resolver()

plugin = Plugin(
    resolver.get_DockerStatsClient(),
    resolver.get_DockerFormatter(),
    resolver.get_ContainerStatsStreamPool(),
    exporter
)

collectd.register_config(plugin.configure)
collectd.register_read(plugin.read)
