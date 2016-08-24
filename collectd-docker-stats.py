#!/usr/bin/python

import collectd

from lib.Collectd.Exporter import Exporter
from lib.Collectd.Plugin import Plugin

exporter = Exporter(collectd)

plugin = Plugin(exporter, collectd)

collectd.register_config(plugin.configure)
collectd.register_init(plugin.init)
