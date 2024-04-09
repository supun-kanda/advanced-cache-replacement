from collections import defaultdict, OrderedDict

class LfuCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # Stores key-value pairs
        self.frequency = defaultdict(OrderedDict)  # Stores keys by frequency
        self.min_freq = 0  # Track the minimum frequency

    def update_frequency(self, key):
        key_frequence = self.cache[key][1]
        self.frequency[key_frequence].pop(key)  # Remove key from current frequency level

        new_key_frequence = key_frequence + 1

        if not self.frequency[key_frequence] and self.min_freq == key_frequence:
            self.min_freq = new_key_frequence

        self.cache[key][1] = new_key_frequence
        self.frequency[new_key_frequence][key] = None

    def get(self, key):
        if key not in self.cache:
            return None
        self.update_frequency(key)  # Update the frequency of the key
        return self.cache[key][0]  # Return the value

    def put(self, key, value):
        if self.capacity <= 0:
            return

        if key in self.cache:
            self.cache[key][0] = value  # Update the value
            self.update_frequency(key)  # Update the frequency
            return

        if len(self.cache) >= self.capacity:
            lfu_key, _ = self.frequency[self.min_freq].popitem(last=False)
            self.cache.pop(lfu_key)

        self.cache[key] = [value, 1]
        self.frequency[1][key] = None
        self.min_freq = 1  # Reset the minimum frequency to 1