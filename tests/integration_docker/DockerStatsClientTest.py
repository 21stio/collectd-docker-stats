import unittest

from lib.DependencyResolver import DependencyResolver

class DockerStatsClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dockerStatsClient = DependencyResolver.get_Resolver().get_DockerStatsClient()
        cls.dockerFormatter = DependencyResolver.get_Resolver().get_DockerFormatter()
        cls.containers = cls.dockerStatsClient.get_containers()
        cls.container_ids = cls.dockerFormatter.get_container_ids(cls.containers)

    def setUp(self):
        self.cls = DockerStatsClientTest

    def test_get_running_containers(self):
        containers = self.cls.dockerStatsClient.get_containers()

        self.assertTrue('Id' in containers[0])
        self.assertTrue('Names' in containers[0])

    def test_get_container_stats(self):
        stats = self.cls.dockerStatsClient.get_container_stats(self.cls.container_ids)

        self.assertTrue('memory_stats' in stats.values()[0])