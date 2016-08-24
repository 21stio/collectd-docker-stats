import unittest

from lib.DependencyResolver import DependencyResolver


class DockerFormatterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dockerStatsClient = DependencyResolver.get_Resolver().get_DockerStatsClient()
        cls.dockerFormatter = DependencyResolver.get_Resolver().get_DockerFormatter()
        cls.containers = cls.dockerStatsClient.get_containers()
        cls.container_names = cls.dockerFormatter.get_container_names(cls.containers)

    def setUp(self):
        self.cls = DockerFormatterTest

    def test_process_stats(self):
        stats = self.cls.dockerStatsClient.get_container_stats(self.cls.container_names)

        processed_stats = self.cls.dockerFormatter.process_stats(stats)

        self.assertTrue('memory_stats.limit' in processed_stats['all'])

        del(processed_stats['all'])

        self.assertTrue('memory_stats.limit' not in processed_stats.values()[0])
        self.assertTrue('memory_stats.usage' in processed_stats.values()[0])
