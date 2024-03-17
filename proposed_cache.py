from collections import OrderedDict
import numpy as np

class ProposedCache():
    def __init__(self, capacity, model):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.model = model

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                key = self.get_eviction_key(self.cache)
                if(key>0):
                  self.cache.pop(key)
                  self.cache[key] = value
                return
            else:
              self.cache[key] = value

    def get_eviction_key(self, cache):
      cache_keys = list(cache.keys())
      predict_array = self.model.predict(np.array(cache_keys).reshape(1,500))
      predict_index = np.argmax(predict_array)
      return cache_keys[predict_index] if predict_index<self.capacity else -1