class DockerStatsClient:

    def __init__(self, dockerClient, containerStatsStreamPool):
        self.dockerClient = dockerClient
        self.containerStatsStreamPool = containerStatsStreamPool

    def get_containers(self):
        return self.dockerClient.containers()

    def get_container_stats(self, container_ids):
        stats = {}
        for containers_id in container_ids:
            stream = self.containerStatsStreamPool.get_ContainerStatsStream(containers_id)

            stats[containers_id] = stream.get_stats()

        return stats
