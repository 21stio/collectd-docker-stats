class Plugin:

    def __init__(self, dockerStatsClient, dockerFormatter, containerStatsStreamPool, exporter):
        self.dockerStatsClient = dockerStatsClient
        self.dockerFormatter = dockerFormatter
        self.containerStatsStreamPool = containerStatsStreamPool
        self.exporter = exporter

        self.includes = []
        self.excludes = []

    def configure(self, conf):
        for node in conf.children:
            try:
                if node.key == 'SocketUrl':
                    self.socket_url = node.values[0]
                elif node.key == 'Timeout':
                    self.timeout = int(node.values[0])
            except Exception as e:
                raise Exception('Failed to load the configuration {0} due to {1}'.format(node.key, e))

    def read(self):
        containers = self.dockerStatsClient.get_containers()

        running_containers = self.dockerFormatter.get_running_containers(containers)

        running_container_ids = self.dockerFormatter.get_container_ids(running_containers)

        running_container_names = self.dockerFormatter.get_container_names(running_containers)

        raw_stats = self.dockerStatsClient.get_container_stats(running_container_ids)

        processed_stats = self.dockerFormatter.process_stats(running_container_names, raw_stats)

        for container_name, container_stats in processed_stats.iteritems():
            for metric_name, metric_value in container_stats.iteritems():
                self.exporter.export(container_name, metric_name, metric_value)

        self.containerStatsStreamPool.keep_streams_running(running_container_ids)