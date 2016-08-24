import ContainerStatsStream


class ContainerStatsStreamPool:

    def __init__(self, dockerClient):
        self.dockerClient = dockerClient
        self.container_stats_streams = {}

    def get_ContainerStatsStream(self, container_name):
        if container_name not in self.container_stats_streams:
            self.container_stats_streams[container_name] = ContainerStatsStream.ContainerStatsStream(self.dockerClient, container_name)

        return self.container_stats_streams[container_name]

    def keep_streams_running(self, keep_container_names):
        terminated_ids = []

        for container_name in self.container_stats_streams.keys():
            if container_name not in keep_container_names:
                terminated_ids.append(container_name)

        for container_name in terminated_ids:
            self.container_stats_streams[container_name].running = False
