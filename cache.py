class Cache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}

    def get(self, key):
        return self.cache.get(key, None)

    def put(self, key, value):
        if len(self.cache) >= self.capacity:
            self.evict()
        self.cache[key] = value

    def evict(self):
        # Example: Random eviction
        key_to_evict = random.choice(list(self.cache.keys()))
        del self.cache[key_to_evict]
