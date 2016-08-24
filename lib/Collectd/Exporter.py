import time
import dateutil.parser

class Exporter:

    def __init__(self, collectd):
        self.collectd = collectd

    def export(self, container_name, metric_name, metric_value, timestamp=None):
        export = self.collectd.Values()

        export.plugin = 'docker'

        export.plugin_instance = container_name

        export.type = metric_name
        export.type_instance = None

        if timestamp:
            export.time = time.mktime(dateutil.parser.parse(timestamp).timetuple())
        else:
            export.time = time.time()

        export.meta = {'true': 'true'}

        export.values = [metric_value]
        export.dispatch()