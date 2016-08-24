import unittest
import threading

from lib.DependencyResolver import DependencyResolver

class ContainerStatsStreamPoolTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.containerStatsStreamPool = DependencyResolver.get_Resolver().get_ContainerStatsStreamPool()
        cls.dockerFormatter = DependencyResolver.get_Resolver().get_DockerFormatter()
        cls.dockerStatsClient = DependencyResolver.get_Resolver().get_DockerStatsClient()
        cls.containers = cls.dockerStatsClient.get_containers()

    def setUp(self):
        self.cls = ContainerStatsStreamPoolTest

    def test_get_ContainerStatsStream(self):
        container_id = self.cls.dockerFormatter.get_container_id(self.cls.containers[0])

        stream = self.cls.containerStatsStreamPool.get_ContainerStatsStream(container_id)

        self.assertTrue(isinstance(stream, threading.Thread))

    def test_keep_streams_running(self):
        running_containers = self.cls.dockerFormatter.get_running_containers(self.cls.containers)

        running_container_ids = self.cls.dockerFormatter.get_container_ids(running_containers)

        running_streams = []
        for container_id in running_container_ids:
            stream = self.cls.containerStatsStreamPool.get_ContainerStatsStream(container_id)
            running_streams.append(stream)

        fake_stream = self.cls.containerStatsStreamPool.get_ContainerStatsStream('abc')

        self.assertTrue(fake_stream.running)

        self.cls.containerStatsStreamPool.keep_streams_running(running_container_ids)

        self.assertFalse(fake_stream.running)

        for stream in running_streams:
            self.assertTrue(stream.running)
