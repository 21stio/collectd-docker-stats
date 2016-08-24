import unittest

from lib.DependencyResolver import DependencyResolver


class DockerFormatterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dockerStatsClient = DependencyResolver.get_Resolver().get_DockerStatsClient()
        cls.dockerFormatter = DependencyResolver.get_Resolver().get_DockerFormatter()
        cls.containers = cls.dockerStatsClient.get_containers()
        cls.container_ids = cls.dockerFormatter.get_container_ids(cls.containers)

    def setUp(self):
        self.cls = DockerFormatterTest

    def test_process_stats(self):
        stats = self.cls.dockerStatsClient.get_container_stats(self.cls.container_ids)

        container_names = self.cls.dockerFormatter.get_container_names(self.containers)

        processed_stats = self.cls.dockerFormatter.process_stats(container_names, stats)

        self.assertTrue('memory_stats.limit' in processed_stats['all'])

        print processed_stats

        del(processed_stats['all'])
        random_container_name = container_names.values()[0]

        self.assertTrue('memory_stats.limit' not in processed_stats[random_container_name])
        self.assertTrue('memory_stats.usage' in processed_stats[random_container_name])