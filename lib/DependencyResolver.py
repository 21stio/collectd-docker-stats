from DictHelper import DictHelper
from ContainerStatsStreamPool import ContainerStatsStreamPool
from DockerFormatter import DockerFormatter
from DockerStatsClient import DockerStatsClient
import docker
from distutils.version import StrictVersion


class DependencyResolver:
    resolver = None

    @classmethod
    def get_Resolver(cls, socket_url=None, timeout=None):
        if cls.resolver is None:
            cls.resolver = DependencyResolver(socket_url, timeout)

        return cls.resolver

    def __init__(self, socket_url=None, timeout=None):
        self.socket_url = socket_url or 'unix://var/run/docker.sock'
        self.timeout = timeout or 5
        self.min_api_version = '1.17'

        self.dockerClient = None
        self.dictHelper = None
        self.dockerFormatter = None
        self.containerStatsStreamPool = None
        self.dockerStatsClient = None

    def get_DockerClient(self):
        if self.dockerClient is None:
            self.dockerClient = docker.Client(
                base_url=self.socket_url,
                version=self.min_api_version
            )

            self.dockerClient.timeout = self.timeout

            daemon_version = self.dockerClient.version()['ApiVersion']
            if StrictVersion(daemon_version) < StrictVersion(self.min_api_version):
                raise Exception('Docker daemon at {0} does not support container statistics!'.format(self.socket_url))

        print "started docker-py client socket_url: {0} version: {1}".format(self.socket_url, self.min_api_version)

        return self.dockerClient

    def get_ContainerStatsStreamPool(self):
        if self.containerStatsStreamPool is None:
            self.containerStatsStreamPool = ContainerStatsStreamPool(self.get_DockerClient())

        return self.containerStatsStreamPool

    def get_DictHelper(self):
        if self.dictHelper is None:
            self.dictHelper = DictHelper()

        return self.dictHelper

    def get_DockerFormatter(self):
        if self.dockerFormatter is None:
            self.dockerFormatter = DockerFormatter(self.get_DictHelper())

        return self.dockerFormatter

    def get_DockerStatsClient(self):
        if self.dockerStatsClient is None:
            self.dockerStatsClient = DockerStatsClient(self.get_DockerClient(), self.get_ContainerStatsStreamPool())

        return self.dockerStatsClient
