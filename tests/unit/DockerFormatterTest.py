import unittest

from lib.DependencyResolver import DependencyResolver


class DockerFormatterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dockerFormatter = DependencyResolver.get_Resolver().get_DockerFormatter()

    def setUp(self):
        self.cls = DockerFormatterTest

    def test_get_container_name(self):
        container = {}
        container['Names'] = ['/test', "/test_abc"]

        container_name = self.cls.dockerFormatter.get_container_name(container)
        self.assertEqual(container_name, 'test')

    def test_get_global_stats(self):
        resolved_stats = {
            'container_1': {
                'memory.usage': 84,
                'memory.total': 100,
                'unique': 100
            },
            'container_2': {
                'memory.usage': 4,
                'memory.total': 100
            }
        }

        global_stats = self.cls.dockerFormatter.get_global_stats(resolved_stats)

        self.assertTrue('memory.total' in global_stats)
        self.assertTrue('memory.usage' not in global_stats)
        self.assertTrue('unique' not in global_stats)
        self.assertTrue(global_stats['memory.total'] == 100)

        resolved_stats = {
            'container_1': {
                'memory.usage': 84,
                'memory.total': 100,
                'unique': 100
            }
        }

        global_stats = self.cls.dockerFormatter.get_global_stats(resolved_stats)

        self.assertTrue(len(global_stats.keys()) == 0)

    def test_get_resolved_stats(self):
        stats = {
            'memory': {
                'total': 21
            }
        }

        resolved_stats = self.cls.dockerFormatter.get_resolved_stats(stats)

        self.assertTrue('memory.total' in resolved_stats)
        self.assertTrue(resolved_stats['memory.total'] == 21)

    def test_remove_global_stats(self):
        resolved_stats = {
            'memory.usage': 42,
            'memory.total': 100
        }

        global_stats = {
            'memory.total': 100
        }

        stats_without_global_stats = self.cls.dockerFormatter.remove_global_stats(resolved_stats, global_stats)

        self.assertTrue('memory.usage' in stats_without_global_stats)
        self.assertTrue('memory.total' not in stats_without_global_stats)

    def test_get_running_container(self):
        containers = [
            {
                'Status': 'Up 1 hour'
            },
            {
                'Status': 'Restarting'
            }
        ]

        running_containers = self.cls.dockerFormatter.get_running_containers(containers)

        self.assertTrue(len(running_containers) == 1)
        self.assertTrue(running_containers[0]['Status'].startswith('Up'))

    def test_calculate_cpu_percentage(self):
        stats = {
            "precpu_stats": {
                "cpu_usage": {
                    "total_usage": 19242341735,
                    "percpu_usage": [
                        19242341735
                    ],
                    "usage_in_kernelmode": 2950000000,
                    "usage_in_usermode": 14990000000
                },
                "system_cpu_usage": 47493870000000,
                "throttling_data": {
                    "periods": 0,
                    "throttled_periods": 0,
                    "throttled_time": 0
                }
            },
            "cpu_stats": {
                "cpu_usage": {
                    "total_usage": 19242433202,
                    "percpu_usage": [
                        19242433202
                    ],
                    "usage_in_kernelmode": 2950000000,
                    "usage_in_usermode": 14990000000
                },
                "system_cpu_usage": 47494860000000,
                "throttling_data": {
                    "periods": 0,
                    "throttled_periods": 0,
                    "throttled_time": 0
                }
            }
        }

        cpu_percentage = self.cls.dockerFormatter.calculate_cpu_percentage(stats)

        self.assertTrue(cpu_percentage > 0)
        self.assertTrue(cpu_percentage < 100)

    def test_calculate_memory_percentage(self):
        stats = {
            "memory_stats": {
                "usage": 2,
                "limit": 10
            }
        }

        memory_percentage = self.cls.dockerFormatter.calculate_memory_percentage(stats)

        self.assertTrue(memory_percentage == 20)

    def test_get_container_names(self):
        containers = [
            {
                'Id': 'a7b',
                'Names': ['/nginx']
            }
        ]

        container_names = self.cls.dockerFormatter.get_container_names(containers)

        self.assertTrue('nginx' in container_names)
