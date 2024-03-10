import unittest

from frozen_cache import FrozenCacheDev

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
        print(self.frozen_cache.future_map)
        self.assertEqual(-1, result)
    
    def test_frozen_cache_4(self):
        self.frozen_cache.put(5,5,3)
        self.frozen_cache.put(6,6,4)
        self.frozen_cache.put(7,7,5)
        self.assertEqual(list(self.frozen_cache.cache.keys()), [2,3,4])

    def test_frozen_cache_5(self):
        result = self.frozen_cache.put(2, 2, 3)
        self.assertEqual(-1, result)
    
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


if __name__ == '__main__':
    unittest.main()