class DockerFormatter:

    def __init__(self, dictHelper):
        self.dictHelper = dictHelper

    def get_container_name(self, container):
        names = container['Names']

        for name in names:
            split = name.split('/')
            if len(split) == 2:
                return split[1]
        raise Exception('can not find valid container name in {names}'.format(names=names))

    def get_resolved_stats(self, stats):
        return self.dictHelper.resolve_dimensions(stats)

    def remove_global_stats(self, stats, global_stats):
        for metric in global_stats.keys():
            del (stats[metric])

        return stats

    def get_global_stats(self, stats):
        stats = stats.values()

        return self.dictHelper.find_same_value_keys(stats)

    def get_container_names(self, containers):
        names = []

        for container in containers:
            names.append(self.get_container_name(container))

        return names

    def get_running_containers(self, containers):
        running_containers = []

        for container in containers:
            if str(container['Status']).startswith('Up'):
                running_containers.append(container)

        return running_containers

    def calculate_cpu_percentage(self, stats):
        cpu_percentage = 0.0

        if 'precpu_stats' in stats:
            previous_stats = stats['precpu_stats']

            current_total_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            current_system_cpu_usage = stats['cpu_stats']['system_cpu_usage']

            previous_total_usage = previous_stats['cpu_usage']['total_usage']
            previous_system_cpu_usage = previous_stats['system_cpu_usage']

            cpu_delta = current_total_usage - previous_total_usage
            system_delta = current_system_cpu_usage - previous_system_cpu_usage

            cpu_count = len(stats['cpu_stats']['cpu_usage']['percpu_usage'])

            if system_delta > 0 and cpu_delta > 0:
                cpu_percentage = 100.0 * cpu_delta / system_delta * cpu_count

        return cpu_percentage

    def calculate_memory_percentage(self, stats):
        usage = stats['memory_stats']['usage']
        limit = stats['memory_stats']['limit']

        return 100.0 * usage / limit

    def process_stats(self, all_stats):
        resolved_stats = {}
        for container_name, container_stats in all_stats.iteritems():
            container_stats['cpu_stats']['percentage'] = self.calculate_cpu_percentage(container_stats)
            container_stats['memory_stats']['percentage'] = self.calculate_memory_percentage(container_stats)

            resolved_stats[container_name] = self.get_resolved_stats(container_stats)

        global_stats = self.get_global_stats(resolved_stats)

        stats_without_global_stats = {}
        for container_name, container_stats in resolved_stats.iteritems():
            stats_without_global_stats[container_name] = self.remove_global_stats(container_stats, global_stats)

        stats = stats_without_global_stats

        stats['all'] = global_stats

        return stats
