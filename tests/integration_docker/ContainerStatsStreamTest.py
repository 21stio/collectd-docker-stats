import unittest

from lib.DependencyResolver import DependencyResolver


class ContainerStatsStreamTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.containerStatsStreamPool = DependencyResolver.get_Resolver().get_ContainerStatsStreamPool()
        cls.dockerFormatter = DependencyResolver.get_Resolver().get_DockerFormatter()
        cls.dockerStatsClient = DependencyResolver.get_Resolver().get_DockerStatsClient()

    def setUp(self):
        self.cls = ContainerStatsStreamTest

    def test_get_stats(self):
        containers = self.cls.dockerStatsClient.get_containers()
        container_name = self.cls.dockerFormatter.get_container_name(containers[0])

        stats = self.cls.containerStatsStreamPool.get_ContainerStatsStream(container_name).get_stats()

        self.assertTrue('cpu_stats' in stats)
        self.assertTrue('memory_stats' in stats)
