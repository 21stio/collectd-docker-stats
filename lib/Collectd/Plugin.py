class Plugin:

    def __init__(self, dockerStatsClient, dockerFormatter, containerStatsStreamPool, exporter):
        self.dockerStatsClient = dockerStatsClient
        self.dockerFormatter = dockerFormatter
        self.containerStatsStreamPool = containerStatsStreamPool
        self.exporter = exporter

        self.includes = []
        self.excludes = []

    def read(self):
        containers = self.dockerStatsClient.get_containers()

        running_containers = self.dockerFormatter.get_running_containers(containers)

        running_container_names = self.dockerFormatter.get_container_names(running_containers)

        raw_stats = self.dockerStatsClient.get_container_stats(running_container_names)

        processed_stats = self.dockerFormatter.process_stats(raw_stats)

        for container_name, container_stats in processed_stats.iteritems():
            timestamp = None

            if 'read' in container_stats:
                timestamp = container_stats['read']
                del(container_stats['read'])

            for metric_name, metric_value in container_stats.iteritems():
                self.exporter.export(container_name, metric_name, metric_value, timestamp)

        self.containerStatsStreamPool.keep_streams_running(running_container_names)
