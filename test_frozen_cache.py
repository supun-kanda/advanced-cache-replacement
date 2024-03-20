import unittest

from frozen_cache import FrozenCacheDev, remove_values_less_than, derive_data_index_map
from collections import OrderedDict

class TestFrozenCache(unittest.TestCase):
    def setUp(self):
        self.cache = [2,3,4]
        self.frozen_cache = FrozenCacheDev(3,[2,3,4,5,6,7])
        self.frozen_cache.put(2,2,0)
        self.frozen_cache.put(3,3,1)
        self.frozen_cache.put(4,4,2)

    def test_frozen_cache_base(self):
        self.assertEqual(self.cache, list(self.frozen_cache.cache.keys()))

    def test_frozen_cache_1(self):
        self.assertEqual(self.cache, list(self.frozen_cache.cache.keys()))
        self.assertEqual(3, len(self.frozen_cache.cache.keys()))
    
    def test_frozen_cache_2(self):
        result = self.frozen_cache.put(123, 123, 3)
        self.assertEqual(-1, result)
        
    def test_frozen_cache_3(self):
        result = self.frozen_cache.put(5, 5, 3)
        self.assertEqual(-1, result)
    
    def test_frozen_cache_4(self):
        self.frozen_cache.put(5,5,3)
        self.frozen_cache.put(6,6,4)
        self.frozen_cache.put(7,7,5)
        self.assertEqual(list(self.frozen_cache.cache.keys()), [2,3,4])

    def test_frozen_cache_5(self):
        result = self.frozen_cache.put(2, 2, 3)
        self.assertEqual(-2, result)
    
    def test_frozen_cache_6(self):
        self.cache = [2,3,4]
        self.frozen_cache = FrozenCacheDev(3, [2,3,4,5,2,3,4,5,2,3,4,5])
        self.frozen_cache.put(2,2,0)
        self.frozen_cache.put(3,3,1)
        self.frozen_cache.put(4,4,2)
        print(2,self.frozen_cache.cache, self.frozen_cache.future_map)
        self.frozen_cache.put(5,5,3)
        print(3,self.frozen_cache.cache, self.frozen_cache.future_map)
        self.frozen_cache.put(2,2,4)
        print(4,self.frozen_cache.cache, self.frozen_cache.future_map)
        self.frozen_cache.put(3,3,5)
        print(5,self.frozen_cache.cache, self.frozen_cache.future_map)
        self.frozen_cache.put(4,4,6)
        print(6,self.frozen_cache.cache, self.frozen_cache.future_map)
        self.frozen_cache.put(5,5,7)
        print(7,self.frozen_cache.cache, self.frozen_cache.future_map)
        self.assertEqual(3, len(self.frozen_cache.cache))
    
    def test_remove_values_less_than(self):
        dictionary = {1: [0,1,7], 2: [5,8,9], 3: [2], 4: [3,4,6]}

        remove_values_less_than(dictionary, 5)
        self.assertEqual(dictionary, {1:[7], 2:[8,9], 4:[6]})

    def test_derive_data_index_map(self):
        dataset = [2,3,4,5,2,3,4,5,2,3,4,5]

        result = derive_data_index_map(dataset)
        self.assertEqual(result,  OrderedDict({2:[0,4,8], 3:[1,5,9], 4:[2,6,10],5:[3,7,11]}))

    def test_get_removable_address(self):
        self.frozen_cache = FrozenCacheDev(3, [2,3,4,5,2,3,4,5,2,3,4,5])
        self.assertEqual(self.frozen_cache.future_map,  OrderedDict({2:[0,4,8], 3:[1,5,9], 4:[2,6,10],5:[3,7,11]}))
        self.frozen_cache.put(2,2,0)
        self.assertEqual(self.frozen_cache.future_map,  OrderedDict({2:[0,4,8], 3:[1,5,9], 4:[2,6,10],5:[3,7,11]}))
        self.frozen_cache.put(3,3,1)
        self.frozen_cache.put(4,4,2)
        self.frozen_cache.put(5,5,3)
        self.assertEqual(self.frozen_cache.future_map,  OrderedDict({2:[4,8], 3:[5,9], 4:[6,10],5:[7,11]}))
        self.frozen_cache.put(2,2,4)
        self.frozen_cache.put(3,3,5)
        self.frozen_cache.put(4,4,6)
        self.frozen_cache.put(5,5,7)
    
    def test_get_removable_address_2(self):
        self.frozen_cache = FrozenCacheDev(1, [6,5,4,2,2,4,5,2,4,4,5])
        self.assertEqual(self.frozen_cache.future_map,  OrderedDict({6:[0], 5:[1,6,10], 4:[2,5,8,9],2:[3,4,7]}))
        self.frozen_cache.put(6,6,0)
        self.frozen_cache.put(5,5,1)
        self.frozen_cache.put(4,4,2)
        self.frozen_cache.put(2,2,3)
        self.frozen_cache.put(2,2,4)
        self.frozen_cache.put(4,4,5)
        self.frozen_cache.put(5,5,6)
        self.assertEqual(self.frozen_cache.future_map,  OrderedDict({5:[10],4:[8,9],2:[7]}))

    
    def test_get_removable_address_3(self):
        self.frozen_cache = FrozenCacheDev(3, [2,3,4,5,2,3,4,5,2,3,4,5])
        self.frozen_cache.put(2,2,0)
        self.frozen_cache.put(3,3,1)
        self.frozen_cache.put(4,4,2)
        value = self.frozen_cache.put(5,5,3)
        self.assertEqual(self.frozen_cache.future_map,  OrderedDict({2:[4,8], 3:[5,9], 4:[6,10],5:[7,11]}))
        self.assertEqual(value, 4)
    
    def test_get_fi_score(self):
        self.frozen_cache = FrozenCacheDev(3, [2,3,4,5,2,3,4,5,2,3,4,5])
        self.frozen_cache.put(2,2,0)
        self.frozen_cache.put(3,3,1)
        self.frozen_cache.put(4,4,2)
        dict = OrderedDict({2:[4,8], 3:[5,9], 4:[6,10],5:[3,7,11]})
        result = self.frozen_cache.get_fi_score(dict[2], 2)

        self.assertEqual(result, 2/3 + 8/10)
        self.assertEqual(self.frozen_cache.get_fi_score([0,4,8], 0), 2)

if __name__ == '__main__':
    unittest.main()