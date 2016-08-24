import time
import dateutil.parser


class Exporter:

    skip = ['precpu_stats']

    def __init__(self, collectd):
        self.collectd = collectd

    def export(self, container_name, metric_name, metric_value, timestamp=None):
        type = self.get_type(metric_name)

        if self.should_skip(type):
            return

        export = self.collectd.Values()

        export.plugin = 'docker'

        export.plugin_instance = container_name

        export.type = type
        export.type_instance = self.get_type_instace(metric_name)

        if timestamp:
            export.time = time.mktime(dateutil.parser.parse(timestamp).timetuple())
        else:
            export.time = time.time()

        export.meta = {'true': 'true'}

        export.values = [metric_value]
        export.dispatch()

    def get_type(self, metric_name):
        return metric_name.split('.')[0]

    def get_type_instace(self, metric_name):
        metric_parts = metric_name.split('.')
        metric_parts.pop(0)

        if metric_parts[0] == 'stats':
            metric_parts.pop(0)

        return ".".join(metric_parts)

    def should_skip(self, type):
        return type in ['precpu_stats']
