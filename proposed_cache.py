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
            # Update the value and move the key to the end to mark it as most recently used
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                address = self.get_removable_address(self.cache)

                if address >= 0:
                    self.cache.pop(address)
                    self.cache[key] = value

                return address

            self.cache[key] = value
        return -2

    def get_removable_address(self, cache):
      cache_keys = list(cache.keys())
      predict_array = self.model.predict(np.array(cache_keys).reshape(1, self.capacity), verbose = 0)
      predict_index = np.argmax(predict_array)
      return cache_keys[predict_index] if predict_index<self.capacity else -1