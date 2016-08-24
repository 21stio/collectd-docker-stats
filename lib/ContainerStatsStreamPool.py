import ContainerStatsStream

class ContainerStatsStreamPool:

    def __init__(self, dockerClient):
        self.dockerClient = dockerClient
        self.container_stats_streams = {}

    def get_ContainerStatsStream(self, container_id):
        if container_id not in self.container_stats_streams:
            self.container_stats_streams[container_id] = ContainerStatsStream.ContainerStatsStream(self.dockerClient, container_id)

        return self.container_stats_streams[container_id]

    def keep_streams_running(self, keep_container_ids):
        terminated_ids = []

        for container_id in self.container_stats_streams.keys():
            if container_id not in keep_container_ids:
                terminated_ids.append(container_id)

        for container_id in terminated_ids:
            self.container_stats_streams[container_id].running = False