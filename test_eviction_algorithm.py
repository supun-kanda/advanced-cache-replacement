import unittest

from eviction_algorithm import get_eviction_address

class TestEvictionAlgorithm(unittest.TestCase):
    def setUp(self):
        self.cache = [2,3,4,5,63]
        self.future = [4,5,324523,342343,4323,23,232]

    def test_eviction_algorithm_fundamental_checks(self):
        key = 5
        result = get_eviction_address(key, self.cache, self.future)
        self.assertEqual(result, -1)
    
    def test_eviction_algorithm_1(self):
        key = 123
        result = get_eviction_address(key, self.cache, self.future)
        self.assertEqual(result, 2)

    def test_eviction_algorithm_2(self):
        key = 123
        self.cache = [2,3,4,5,63]
        self.future = [2,3,4,5,63,4,5,324523,342343,4323,23,232]
        result = get_eviction_address(key, self.cache, self.future)
        self.assertEqual(result, -1)

if __name__ == '__main__':
    unittest.main()