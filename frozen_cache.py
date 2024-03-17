from collections import OrderedDict

def derive_data_index_map(dataset):
    data_map = OrderedDict()
    for index, value in enumerate(dataset):
        if value in data_map:
            data_map[value].append(index)
        else:
            data_map[value] = [index]
    return data_map

def remove_values_less_than(d, threshold):
    empty_keys = []

    for key, values in d.items():
        d[key] = [value for value in values if value > threshold]

        if not d[key]:
            empty_keys.append(key)

    for key in empty_keys:
        del d[key]

class FrozenCacheDev():
    def __init__(self, capacity, data_set):
        self.capacity = capacity
        self.cache = OrderedDict()
        print("getting the data_set file ready")
        self.data_set = data_set
        self.data_len = len(self.data_set)
        print("deriving the data map")
        self.future_map = derive_data_index_map(self.data_set)

    def get(self, key):
        if key not in self.cache:
            return None
        # Move the accessed key to the end to mark it as most recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value, time_step):
        if key in self.cache:
            # Update the value and move the key to the end to mark it as most recently used
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                address = self.get_removable_address(key, time_step)

                if address > 0:
                    self.cache.pop(address)
                    self.cache[key] = value

                return address

            self.cache[key] = value
        return -2
    
    def get_fi_score(self, values, time_step):
        return (len(values) / self.capacity) + ((self.data_len - min(values)) / (self.data_len - time_step))


    def get_removable_address(self, request, time_step):
        remove_values_less_than(self.future_map, time_step)

        if request not in self.future_map:
            return -1

        cache_future = {}
        for key in self.cache:
            if key in self.future_map:
                cache_future[key] = self.future_map[key]
            else:
                return key

        fi_score = {key: self.get_fi_score(values, time_step) for key, values in cache_future.items()}
        return min(fi_score, key=fi_score.get)