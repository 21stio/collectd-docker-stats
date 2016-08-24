from lib.DependencyResolver import DependencyResolver

class Plugin:

    def __init__(self, exporter, collectd):
        self.exporter = exporter
        self.socket_url = None
        self.timeout = None
        self.collectd = collectd

    def configure(self, conf):
        print conf
        for node in conf.children:
            try:
                if node.key == 'SocketUrl':
                    self.socket_url = node.values[0]
                elif node.key == 'Timeout':
                    self.timeout = int(node.values[0])
            except Exception as e:
                raise Exception('Failed to load the configuration {0} due to {1}'.format(node.key, e))

    def init(self):
        self.collectd.register_read(self.read)

    def read(self):
        resolver = DependencyResolver.get_Resolver(self.socket_url, self.timeout)

        containers = resolver.get_DockerStatsClient().get_containers()

        running_containers = resolver.get_DockerFormatter().get_running_containers(containers)

        running_container_names = resolver.get_DockerFormatter().get_container_names(running_containers)

        raw_stats = resolver.get_DockerStatsClient().get_container_stats(running_container_names)

        processed_stats = resolver.get_DockerFormatter().process_stats(raw_stats)

        for container_name, container_stats in processed_stats.iteritems():
            timestamp = None

            if 'read' in container_stats:
                timestamp = container_stats['read']
                del(container_stats['read'])

            for metric_name, metric_value in container_stats.iteritems():
                self.exporter.export(container_name, metric_name, metric_value, timestamp)

        resolver.get_ContainerStatsStreamPool().keep_streams_running(running_container_names)
