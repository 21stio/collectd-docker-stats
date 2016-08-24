from DictHelper import DictHelper
from ContainerStatsStreamPool import ContainerStatsStreamPool
from DockerFormatter import DockerFormatter
from DockerStatsClient import DockerStatsClient
import docker
from distutils.version import StrictVersion

class DependencyResolver:

    resolver = None

    @classmethod
    def get_Resolver(cls):
        if cls.resolver is None:
            cls.resolver = DependencyResolver('unix://var/run/docker.sock', '1.17', 5)

        return cls.resolver

    def __init__(self, socket_url, min_api_version, timeout):
        self.socket_url = socket_url
        self.min_api_version = min_api_version
        self.timeout = timeout

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
