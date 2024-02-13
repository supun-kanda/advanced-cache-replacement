from collections import defaultdict

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # Dictionary to store key-value pairs
        self.frequency = defaultdict(int)  # Dictionary to store frequency of each key
        self.min_freq = 0  # Minimum frequency observed in the cache

    def get(self, key):
        if key not in self.cache:
            return None
        # Increment the frequency of the accessed key
        self.frequency[key] += 1
        # Update the minimum frequency if necessary
        self.min_freq = min(self.min_freq, self.frequency[key])
        return self.cache[key]

    def put(self, key, value):
        if self.capacity == 0:
            return
        # If key already exists, update its value and increment its frequency
        if key in self.cache:
            self.cache[key] = value
            self.frequency[key] += 1
        else:
            # Evict least frequently used key if cache is at capacity
            if len(self.cache) >= self.capacity:
                self.evict()
            # Add new key-value pair to cache with frequency 1
            self.cache[key] = value
            self.frequency[key] = 1
            # Reset minimum frequency to 1 for new key
            self.min_freq = 1

    def evict(self):
        # Find the key(s) with the minimum frequency
        keys_to_remove = [key for key in self.frequency if self.frequency[key] == self.min_freq]
        # Remove the key(s) from the cache and frequency dictionary
        for key in keys_to_remove:
            del self.cache[key]
            del self.frequency[key]
        # Update the minimum frequency after eviction
        self.min_freq += 1