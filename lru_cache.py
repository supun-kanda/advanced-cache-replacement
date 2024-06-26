from collections import OrderedDict

class LruCache():
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        # Move the accessed key to the end to mark it as most recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            # Update the value and move the key to the end to mark it as most recently used
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                # Evict the least recently used key (first key in OrderedDict)
                try:
                    address = self.cache.popitem(last=False)[0]
                    self.cache[key] = value

                    return address
                except KeyError:
                    print("Key error occured", self.cache)
                    return -1
            self.cache[key] = value
            return -2
