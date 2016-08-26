import collectd

from lib.Docker.DependencyResolver import DependencyResolver as DockerDependencyResolver
from lib.Collectd.DependencyResolver import DependencyResolver as CollectdDependencyResolver


global timeout
global socket_url

timeout = None
socket_url = None


def configure(configuration):
    for node in configuration.children:
        try:
            if node.key == 'SocketUrl':
                global socket_url
                socket_url = node.values[0]
            elif node.key == 'Timeout':
                global timeout
                timeout = int(node.values[0])
        except Exception as e:
            raise Exception('failed to load the configurationiguration {0} due to {1}'.format(node.key, e))


def read():
    containers = docker_dependency_resolver.get_DockerStatsClient().get_containers()

    running_containers = docker_dependency_resolver.get_DockerFormatter().get_running_containers(containers)

    running_container_names = docker_dependency_resolver.get_DockerFormatter().get_container_names(running_containers)

    raw_stats = docker_dependency_resolver.get_DockerStatsClient().get_container_stats(running_container_names)

    processed_stats = docker_dependency_resolver.get_DockerFormatter().process_stats(raw_stats)

    for container_name, container_stats in processed_stats.iteritems():
        timestamp = None

        if 'read' in container_stats:
            timestamp = container_stats['read']
            del (container_stats['read'])

        for metric_name, metric_value in container_stats.iteritems():
            collectd_dependency_resolver.get_Exporter().export(container_name, metric_name, metric_value, timestamp)

    docker_dependency_resolver.get_ContainerStatsStreamPool().keep_streams_running(running_container_names)


def init():
    collectd.register_read(read)


try:
    collectd_dependency_resolver = CollectdDependencyResolver.get_Resolver(collectd)

    docker_dependency_resolver = DockerDependencyResolver.get_Resolver(collectd_dependency_resolver.get_Logger(), socket_url, timeout)

    collectd.register_config(configure)
    collectd.register_init(init)

except Exception as exception:
    collectd.error('collectd-docker-stats-plugin: plugin stopped because of exception: '.format(exception.message))
