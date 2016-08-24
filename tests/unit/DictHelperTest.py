import unittest

from lib.DependencyResolver import DependencyResolver

def print_resolved_stats(stats):
    for metric in sorted(stats):
        print '    ' + metric.ljust(60) + str(stats[metric])

class DictHelperTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dictHelper = DependencyResolver.get_Resolver().get_DictHelper()

    def setUp(self):
        self.cls = DictHelperTest

    def test_findAllDictsSameValueKeys(self):
        _array = [
            {
                "first": 1,
                "second": 1
            },
            {
                "first": 1,
                "second": 2
            },
            {
                "first": 1,
                "second": 3
            },
        ]

        sameValueBag = self.cls.dictHelper.find_same_value_keys(_array)

        self.assertEqual(len(sameValueBag), 1)

        self.assertEqual(sameValueBag['first'], 1)

    def test_resolveDimensions(self):
        _dict = {
            "first_1": 1,
            "first_2": 2,
            "first_3": [1, 2],
            "first_4": {
                "second_1": 1,
                "second_2": 2,
                "second_3": [1, 2],
                "second_4": {
                    "third_1": 1,
                    "third_2": 2,
                    "third_3": [1, 2]
                }
            },
            "first_5": [
                {
                    "second_1": 1,
                    "second_2": 2,
                    "second_3": u"first"
                },
                {
                    "second_1": 1,
                    "second_2": 2,
                    "second_3": u"second"
                }
            ]
        }

        resolved = self.cls.dictHelper.resolve_dimensions(_dict)

        self.assertEqual(len(resolved), 16)

        self.assertEqual(resolved['first_1'], 1)
        self.assertEqual(resolved['first_2'], 2)
        self.assertEqual(resolved['first_3.0'], 1)
        self.assertEqual(resolved['first_3.1'], 2)
        self.assertEqual(resolved['first_4.second_1'], 1)
        self.assertEqual(resolved['first_4.second_2'], 2)
        self.assertEqual(resolved['first_4.second_3.0'], 1)
        self.assertEqual(resolved['first_4.second_3.1'], 2)
        self.assertEqual(resolved['first_4.second_4.third_1'], 1)
        self.assertEqual(resolved['first_4.second_4.third_2'], 2)
        self.assertEqual(resolved['first_4.second_4.third_3.0'], 1)
        self.assertEqual(resolved['first_4.second_4.third_3.1'], 2)
        self.assertEqual(resolved['first_5.first.second_1'], 1)
        self.assertEqual(resolved['first_5.first.second_2'], 2)
        self.assertEqual(resolved['first_5.second.second_1'], 1)
        self.assertEqual(resolved['first_5.second.second_2'], 2)